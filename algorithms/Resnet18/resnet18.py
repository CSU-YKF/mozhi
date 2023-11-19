import os
from PIL import Image
from torch.utils.data import Dataset
from torch.utils.data import DataLoader
from torchvision import transforms
import torchvision
import torch.nn as nn
import torch
import random
from datetime import datetime
import matplotlib.pyplot as plt


class E3CDataset(Dataset):
    def __init__(self, root_dir, result_file, transform=None, train=True):
        """
        初始化数据集。
        :param root_dir: 数据集的目录路径。
        :param result_file: 包含标签信息的文件路径。
        :param transform: 一个用于处理图像的可选变换。
        :param train: 是否为训练集。
        :param train_ratio: 训练集所占的比例。
        """
        self.root_dir = root_dir
        self.transform = transform
        self.image_labels = []
        self.train = train
        self.train_ratio = 0.8

        # 读取 result.txt 文件并解析
        with open(result_file, 'r') as file:
            for line in file:
                parts = line.split('#')
                if len(parts) >= 3:
                    folder_name = parts[0].strip()
                    img_name = parts[1].strip()
                    label = float(parts[2].strip())  # 假设标签是一个浮点数
                    img_path = os.path.join(root_dir, folder_name, img_name)
                    self.image_labels.append((img_path, label))
        # 随机划分训练集和验证集
        random.shuffle(self.image_labels)
        if self.train:
            self.image_labels = self.image_labels[:int(len(self.image_labels) * self.train_ratio)]
        else:
            self.image_labels = self.image_labels[int(len(self.image_labels) * self.train_ratio):]

    def __len__(self):
        """
        返回数据集中的样本总数。
        """
        return len(self.image_labels)

    def __getitem__(self, idx):
        """
        获取指定索引处的图像及其标签。
        :param idx: 样本的索引。
        """
        img_path, label = self.image_labels[idx]
        image = Image.open(img_path).convert('RGB')

        if self.transform:
            image = self.transform(image)

        return image, label


# 图像预处理方式
transform = transforms.Compose([
    # 将图像缩放到 224x224
    transforms.Resize((224, 224)),
    # 转化为灰度图
    transforms.Grayscale(),
    # 将图像转为 PyTorch Tensor
    transforms.ToTensor(),
    # 对图像进行标准化处理
    transforms.Normalize(mean=[0.5], std=[0.5])
])

# 加载数据集，划分训练集和验证集，并进行数据预处理
train_dataset = E3CDataset(root_dir='./E3C', result_file='./result_中位数处理.txt', transform=transform)
test_dataset = E3CDataset(root_dir='./E3C', result_file='./result_中位数处理.txt', transform=transform, train=False)

# 加载数据集，并进行数据预处理
batch_size = 64
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=True)

# 导入网络模型
resnet = torchvision.models.resnet18(weights=None)
# 修改网络结构，使其适用于E3C数据集
resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
resnet.fc = nn.Linear(512, 1)
# cpu or gpu
device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
resnet.to(device)
# 定义超参数
EPOCH = 50
BATCH_SIZE = 64
LR = 0.003
# 定义损失函数和优化器
criterion = nn.MSELoss()
optimizer = torch.optim.Adam(resnet.parameters(), lr=LR)
# 训练网络并输出损失值,并绘制损失函数曲线，以及测试集上的RMSE
losses = []
rmse = []
steps = []
epoches = []
for epoch in range(EPOCH):
    for step, (x, y) in enumerate(train_dataloader):
        x = x.to(device)
        y = y.to(device).float().reshape(-1, 1)
        output = resnet(x)
        loss = criterion(output, y)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        if step % 10 == 0:
            print('Time:', datetime.now(), '| Epoch: ', epoch, '| Step: ', step, '| Loss: ', loss.item())
            # 写入文件
            with open('./loss.txt', 'a') as f:
                f.write('Time:' + str(datetime.now()) + '| Epoch: ' + str(epoch) + '| Step: ' + str(
                    step) + '| Loss: ' + str(loss.item()) + '\n')
            # 绘制损失函数曲线
            losses.append(loss.item())
            steps.append(step + epoch * 110)
            plt.plot(steps, losses)
            plt.xlabel('steps')
            plt.ylabel('loss')
            plt.title('Loss Curve')
            plt.show()
    # 每完成一个epoch测试一下RMSE
    correct = 0
    total = 0
    for x, y in test_dataloader:
        x = x.to(device)
        y = y.to(device).float().reshape(-1, 1)
        output = resnet(x)
        total += y.size(0)
        correct += torch.sqrt(criterion(output, y)).sum().item()
    print('Time:', datetime.now(), '| Epoch: ', epoch, '| Test RMSE: ', correct / total)
    # 写入文件
    with open('./loss.txt', 'a') as f:
        f.write(
            'Time:' + str(datetime.now()) + '| Epoch: ' + str(epoch) + '| Test RMSE: ' + str(correct / total) + '\n')
    # 绘制测试集上的RMSE
    rmse.append(correct / total)
    epoches.append(epoch)
    plt.plot(epoches, rmse)
    plt.xlabel('epoches')
    plt.ylabel('RMSE')
    plt.title('RMSE Curve')
    plt.show()
# 保存最后一张损失函数曲线
plt.plot(steps, losses)
plt.xlabel('steps')
plt.ylabel('loss')
plt.title('Loss Curve')
plt.savefig('./loss.png')
plt.show()

# 保存最后一张RMSE曲线
plt.plot(epoches, rmse)
plt.xlabel('epoches')
plt.ylabel('RMSE')
plt.title('RMSE Curve')
plt.savefig('./RMSE.png')
plt.show()

# 保存模型
torch.save(resnet.state_dict(), './resnet18.pth')
