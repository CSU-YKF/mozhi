import os
import random

import torch
import torchvision
from PIL import Image
from torch.utils.data import Dataset

default_transform = torchvision.transforms.Compose([
    # 将图像缩放到 224x224
    torchvision.transforms.Resize((224, 224)),
    # 将图像转为 PyTorch Tensor
    torchvision.transforms.ToTensor(),
    # 对图像进行标准化处理
    torchvision.transforms.Normalize(mean=[0.6710, 0.6657, 0.6493], std=[0.2706, 0.2712, 0.2746]),
    # 转化为灰度图
    torchvision.transforms.Grayscale(),
])


class E3C(Dataset):
    def __init__(self, root_dir, train=None, transform=default_transform,):
        """
        初始化数据集。
        :param root_dir: 数据集的目录路径。
        :param transform: 一个用于处理图像的可选变换。
        :param train: 是否为训练集。
        """
        super().__init__()
        self.root_dir = root_dir
        self.transform = transform
        self.image_labels = []
        self.train = train
        self.train_ratio = 0.8
        result_file = '../dataset/data/result.txt'

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

        random.shuffle(self.image_labels)

        # 划分训练集和验证集
        if self.train is True:
            self.image_labels = self.image_labels[:int(len(self.image_labels) * self.train_ratio)]
        elif self.train is False:
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
        image = self.transform(image)

        return image, label
