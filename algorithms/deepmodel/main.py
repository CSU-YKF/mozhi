import torch.nn as nn
import torch
import matplotlib.pyplot as plt

from torch.utils.data import DataLoader
from e3c import E3C
from datetime import datetime

from models import resnet, vit

LR = 3e-4
BATCH_SIZE = 64
EPOCH = 100


def main(model=None, epochs=EPOCH, lr=LR, batch_size=BATCH_SIZE):
    time = datetime.now()
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

    # 加载数据集，划分训练集和验证集，并进行数据预处理
    train_dataset = E3C(root_dir='data/E3C', train=True)
    test_dataset = E3C(root_dir='data/E3C', train=False)

    train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, num_workers=16)
    test_dataloader = DataLoader(test_dataset, batch_size=batch_size * 2, num_workers=8)

    # 导入网络模型

    model.to(device)

    # 定义损失函数和优化器
    criterion = nn.MSELoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=lr)
    # 训练网络并输出损失值,并绘制损失函数曲线，以及测试集上的RMSE
    losses = []
    rmse = []
    epoches = []
    for epoch in range(1, epochs + 1):
        loss = 0
        for x, y in train_dataloader:
            x, y = x.to(device), y.to(device).float().reshape(-1, 1)
            output = model(x)
            loss = criterion(output, y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
        time = str(datetime.now().strftime("%Y-%m-%d-%H-%M"))
        print('Time:', time, '| Epoch: ', epoch, '| Loss: ', loss.item())
        # 写入文件
        with open(f'log/loss2.txt', 'a') as f:
            f.write('Time:' + str(time) + '| Epoch: ' + str(epoch) + '| Loss: ' + str(loss.item()) + '\n')
            # 绘制损失函数曲线
        losses.append(loss.item())

        with torch.no_grad():
            # 每完成一个epoch测试一下RMSE
            correct = 0
            total = 0
            for x, y in test_dataloader:
                x, y = x.to(device), y.to(device).float().reshape(-1, 1)
                output = model(x)
                total += y.size(0)
                correct += torch.sqrt(criterion(output, y)).sum().item()
            print('Time:', datetime.now(), '| Epoch: ', epoch, '| Test RMSE: ', correct / total)
            # 写入文件
            with open(f'log/loss{time}.txt', 'a') as f:
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
    plt.savefig(f'log/loss_rmse_{time}.png')
    plt.show()

    # 模型名称
    model_name = str(type(model).__name__)

    # 保存模型
    torch.save(model.state_dict(), f'{model_name}{time}.pth')


if __name__ == '__main__':
    main(model=vit)
    # ResNet16 在1e-3 64 30epoches下的RMSE约为0.009
    # ResNet50 在1e-3 128 20epoches下的RMSE约为0.003
