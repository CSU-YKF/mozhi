import torchvision
import torch.nn as nn
import torch
import matplotlib.pyplot as plt

from torch.utils.data import DataLoader
from e3c import E3C
from datetime import datetime

LR = 1e-3
BATCH_SIZE = 128
EPOCH = 30


def main():
    time = datetime.now()

    # 加载数据集，划分训练集和验证集，并进行数据预处理
    train_dataset = E3C(root_dir='../dataset/data/E3C', train=True)
    test_dataset = E3C(root_dir='../dataset/data/E3C', train=False)

    train_dataloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=16)
    test_dataloader = DataLoader(test_dataset, batch_size=BATCH_SIZE * 2, num_workers=8)

    # 导入网络模型
    resnet = torchvision.models.resnet50(weights=None)
    resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
    resnet.fc = nn.Linear(2048, 1)

    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    resnet.to(device)

    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(resnet.parameters(), lr=LR)
    # 训练网络并输出损失值,并绘制损失函数曲线，以及测试集上的RMSE
    losses = []
    rmse = []
    epoches = []
    for epoch in range(1, EPOCH + 1):
        loss = 0
        for x, y in train_dataloader:
            x, y = x.to(device), y.to(device).float().reshape(-1, 1)
            output = resnet(x)
            loss = criterion(output, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        time = datetime.now()
        print('Time:', time, '| Epoch: ', epoch, '| Loss: ', loss.item())
        # 写入文件
        with open(f'log/loss.txt', 'a') as f:
            f.write('Time:' + str(time) + '| Epoch: ' + str(epoch) + '| Loss: ' + str(loss.item()) + '\n')
            # 绘制损失函数曲线
        losses.append(loss.item())

        with torch.no_grad():
            # 每完成一个epoch测试一下RMSE
            correct = 0
            total = 0
            for x, y in test_dataloader:
                x, y = x.to(device), y.to(device).float().reshape(-1, 1)
                output = resnet(x)
                total += y.size(0)
                correct += torch.sqrt(criterion(output, y)).sum().item()
            print('Time:', datetime.now(), '| Epoch: ', epoch, '| Test RMSE: ', correct / total)
            # 写入文件
            with open(f'log/loss.txt', 'a') as f:
                f.write(
                    'Time:' + str(datetime.now()) + '| Epoch: ' + str(epoch) + '| Test RMSE: ' + str(
                        correct / total) + '\n')
            # 绘制测试集上的RMSE
            rmse.append(correct / total)
            epoches.append(epoch)

    # 创建一个新的图像窗口，包含两个子图
    fig, axs = plt.subplots(2)

    # 在第一个子图中绘制损失函数曲线
    axs[0].plot(epoches, losses)
    axs[0].set(xlabel='steps', ylabel='loss', title='Loss Curve')

    # 在第二个子图中绘制测试集上的RMSE
    axs[1].plot(epoches, rmse)
    axs[1].set(xlabel='epoches', ylabel='RMSE', title='RMSE Curve')

    # 自动调整子图参数，使得子图之间的间距适中
    fig.tight_layout()

    # 保存图像
    plt.savefig('log/loss_and_rmse.png')
    plt.show()

    # 保存模型
    torch.save(resnet.state_dict(), f'resnet50.pth')


if __name__ == '__main__':
    main()
    # ResNet16 在1e-3 64 30epoches下的RMSE约为0.009
    # ResNet50 在1e-3 128 20epoches下的RMSE约为0.003
