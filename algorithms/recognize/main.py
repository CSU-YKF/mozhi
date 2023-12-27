import pickle
import argparse
import torch
import torchvision

from datetime import datetime
from torchvision import transforms
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

from HWDB import HWDB1
from train import train_one_epoch, validate


def parse_args():
    parser = argparse.ArgumentParser(description='Train a model for handwriting recognition')
    parser.add_argument('--train_dir', type=str, default='../dataset/HWDB/Train', help='Directory containing the training .gnt files')
    parser.add_argument('--test_dir', type=str, default='../dataset/HWDB/Test', help='Directory containing the test .gnt files')
    parser.add_argument('--mapping_file', type=str, default='../dataset/HWDB/mapping.pkl', help='Path to the mapping file')
    parser.add_argument('--num_epochs', type=int, default=10, help='Number of epochs to train')
    parser.add_argument('--batch_size', type=int, default=40, help='Batch size for training')
    parser.add_argument('--learning_rate', type=float, default=0.001, help='Learning rate for the optimizer')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    current_time = datetime.now().strftime('%b%d_%H-%M')
    writer = SummaryWriter(log_dir=f'runs/HWDB_experiment/{current_time}')

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    transform = transforms.Compose([
        transforms.ToPILImage(),
        # transforms.Grayscale(),
        transforms.Resize((128, 128)),
        transforms.ToTensor(),
    ])

    train_dataset = HWDB1(gnt_directory=args.train_dir, transform=transform, mapping_file=args.mapping_file)
    test_dataset = HWDB1(gnt_directory=args.test_dir, transform=transform, mapping_file=args.mapping_file)
    train_loader = DataLoader(train_dataset, batch_size=args.batch_size, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=args.batch_size)

    # Load the mapping to determine the number of classes
    with open(args.mapping_file, 'rb') as f:
        mapping = pickle.load(f)
    num_classes = len(mapping['index_to_code'])

    # model = timm.create_model('efficientnetv2_rw_l', pretrained=False, num_classes=num_classes)
    model = torchvision.models.efficientnet.efficientnet_v2_l(weights=None, num_classes=num_classes)
    model.features[0][0] = torch.nn.Conv2d(1, 32, kernel_size=(3, 3), stride=(2, 2), padding=(1, 1), bias=False)
    model.to(device)

    optimizer = torch.optim.Adam(model.parameters(), lr=args.learning_rate)

    # Learning rate scheduler with warm-up
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda epoch: 0.1 ** (epoch // 30))
    # Training loop
    num_epochs = args.num_epochs
    print('Training Begging!')
    for epoch in range(num_epochs):
        train_one_epoch(epoch, num_epochs, model, optimizer, scheduler, train_loader, writer, device)
        auc, acc = validate(epoch, model, test_loader, writer, device)
        print(f'Epoch {epoch+1} completed. AUC: {auc:.4f}, Accuracy: {acc:.4f}')
        torch.save(model.state_dict(), f'runs/HWDB_experiment/model_epoch_{epoch+1}.pth')

        # Record model weights and gradients
        for name, param in model.named_parameters():
            writer.add_histogram(f'Weights/{name}', param, epoch)
            if param.grad is not None:
                writer.add_histogram(f'Gradients/{name}', param.grad, epoch)

        scheduler.step()

    # Close the TensorBoard writer
    writer.close()
    torch.save(model.state_dict(), 'runs/HWDB_experiment/final_model.pth')


if __name__ == '__main__':
    main()
