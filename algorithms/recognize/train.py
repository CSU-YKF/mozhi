import torch
import numpy as np
import torch.nn.functional as F
from sklearn.metrics import roc_auc_score, accuracy_score


# Training function
def train_one_epoch(epoch_index, num_epochs, model, optimizer, scheduler, dataloader, writer, device):
    model.train()
    for batch_index, (images, labels) in enumerate(dataloader):
        images, labels = images.to(device), labels.to(device)

        # Forward pass
        outputs = model(images)
        loss = F.cross_entropy(outputs, labels)

        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        scheduler.step()

        # Record loss and learning rate
        writer.add_scalar('Loss/train', loss.item(), epoch_index * len(dataloader) + batch_index)
        writer.add_scalar('Learning rate', scheduler.get_last_lr()[0], epoch_index * len(dataloader) + batch_index)

        # Print progress
        if (batch_index + 1) % 10 == 0:
            print(f'Epoch [{epoch_index+1}/{num_epochs}], Step [{batch_index+1}/{len(dataloader)}], Loss: {loss.item():.4f}')


# Validation function
def validate(epoch_index, model, dataloader, writer, device):
    model.eval()
    all_labels = []
    all_preds = []
    with torch.no_grad():
        for images, labels in dataloader:
            images, labels = images.to(device), labels.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)

            # Accumulate labels and predictions for AUC and accuracy
            all_labels.extend(labels.cpu().numpy())
            all_preds.extend(F.softmax(outputs, dim=1).cpu().numpy())

    # Calculate AUC and accuracy
    auc = roc_auc_score(all_labels, all_preds, multi_class='ovr')
    acc = accuracy_score(all_labels, np.argmax(all_preds, axis=1))

    # Record metrics
    writer.add_scalar('AUC/validate', auc, epoch_index)
    writer.add_scalar('Accuracy/validate', acc, epoch_index)

    return auc, acc
