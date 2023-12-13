import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from sklearn.metrics import mean_absolute_error, r2_score
from e3c import E3C
from datetime import datetime
import logging

# 参数设置
LR = 1e-3
BATCH_SIZE = 128
EPOCH = 20
DEVICE = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

# 获取当前时间
time = datetime.now().strftime("%Y-%m-%d-%H-%M")

# 设置日志
logging.basicConfig(filename=f'./log/{time}.log', level=logging.INFO, format='%(asctime)s %(message)s')


# 加载数据集
def load_data():
    train_dataset = E3C(root_dir='../dataset/data/E3C', train=True)
    test_dataset = E3C(root_dir='../dataset/data/E3C', train=False)
    train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=16)
    test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE * 2, num_workers=8)
    return train_dataloader, test_dataloader


# 定义训练过程
def train(model, train_dataloader, criterion, optimizer, epoch):
    model.train()
    for x, y in train_dataloader:
        x, y = x.to(DEVICE), y.to(DEVICE).float().reshape(-1, 1)
        output = model(x)
        loss = criterion(output, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    logging.info(f'{epoch}|Loss:{loss.item()}')


# 评估模型
def evaluate(model, test_dataloader, criterion, epoch):
    model.eval()
    with torch.no_grad():
        total_loss, total_mae, total_r2, total_count = 0, 0, 0, 0
        for x, y in test_dataloader:
            x, y = x.to(DEVICE), y.to(DEVICE).float().reshape(-1, 1)
            output = model(x)
            total_loss += torch.sqrt(criterion(output, y)).sum().item()
            total_mae += mean_absolute_error(y.cpu(), output.cpu())
            # total_r2 += r2_score(y.cpu(), output.cpu())
            total_count += y.size(0)
        rmse = total_loss / total_count
        mae = total_mae / total_count
        # r2 = total_r2 / total_count
        logging.info(f'{epoch}|RMSE:{rmse}|MAE:{mae}')


# 主函数
def main():
    train_dataloader, test_dataloader = load_data()

    # 定义模型、损失函数和优化器
    model = torchvision.models.resnet50(weights=None)
    model.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    model.fc = nn.Linear(2048, 1)
    model.to(DEVICE)
    criterion = nn.MSELoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)

    # 训练模型
    for epoch in range(1, EPOCH + 1):
        train(model, train_dataloader, criterion, optimizer, epoch)
        evaluate(model, test_dataloader, criterion, epoch)
        # scheduler.step()

    # 保存模型
    torch.save(model.state_dict(), 'resnet50.pth')


if __name__ == '__main__':
    main()
    # ResNet16 在1e-3 64 30epoches下的RMSE约为0.009
    # ResNet50 在1e-3 128 20epoches下的RMSE约为0.003
