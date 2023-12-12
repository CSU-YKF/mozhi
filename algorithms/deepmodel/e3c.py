import os
import random
<<<<<<< Updated upstream

import torch
import torchvision
=======
import numpy as np
import torchvision

>>>>>>> Stashed changes
from PIL import Image
from torch.utils.data import Dataset

default_transform = torchvision.transforms.Compose([
    # 将图像缩放到 224x224
    torchvision.transforms.Resize((224, 224)),
<<<<<<< Updated upstream
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
=======
    # torchvision.transforms.Normalize(mean=[0.6710, 0.6657, 0.6493], std=[0.2706, 0.2712, 0.2746]),
    # 转化为灰度图
    torchvision.transforms.Grayscale(),
    # 将图像转为 PyTorch Tensor
    torchvision.transforms.ToTensor(),
    # 对图像进行标准化处理
    torchvision.transforms.Normalize(mean=[0.662], std=[0.2721]),
])


class ImageLabelClassifier:
    def __init__(self, image_labels):
        self.lower_bound = None
        self.upper_bound = None
        self.compute_bounds(image_labels)

    def compute_bounds(self, image_labels):
        sorted_labels = np.sort(np.array([label for _, label in image_labels]))
        lower_index = int(len(sorted_labels) * 0.2)
        upper_index = int(len(sorted_labels) * 0.9)
        # self.lower_bound = int(sorted_labels[lower_index])
        self.lower_bound = 6
        self.upper_bound = int(sorted_labels[upper_index])

    def classify(self, label):
        if label <= self.lower_bound:
            return 0
        elif label <= self.upper_bound:
            return 1
        else:
            return 2


class E3C(Dataset):
    def __init__(self, root_dir, train=None, transform=default_transform):
>>>>>>> Stashed changes
        super().__init__()
        self.root_dir = root_dir
        self.transform = transform
        self.image_labels = []
        self.train = train
        self.train_ratio = 0.8
<<<<<<< Updated upstream
        result_file = '../dataset/data/result.txt'

        # 读取 result.txt 文件并解析
=======
        result_file = './data/result.txt'

>>>>>>> Stashed changes
        with open(result_file, 'r') as file:
            for line in file:
                parts = line.split('#')
                if len(parts) >= 3:
<<<<<<< Updated upstream
                    folder_name = parts[0].strip()
                    img_name = parts[1].strip()
                    label = float(parts[2].strip())  # 假设标签是一个浮点数
                    img_path = os.path.join(root_dir, folder_name, img_name)
                    self.image_labels.append((img_path, label))

        random.shuffle(self.image_labels)

        # 划分训练集和验证集
=======
                    folder_name, img_name, label = parts[:3]
                    label = float(label.strip())
                    img_path = os.path.join(root_dir, folder_name.strip(), img_name.strip())
                    self.image_labels.append((img_path, label))

        # random.shuffle(self.image_labels)

>>>>>>> Stashed changes
        if self.train is True:
            self.image_labels = self.image_labels[:int(len(self.image_labels) * self.train_ratio)]
        elif self.train is False:
            self.image_labels = self.image_labels[int(len(self.image_labels) * self.train_ratio):]

<<<<<<< Updated upstream
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
=======
        # 创建分类器实例并计算分界点
        self.classifier = ImageLabelClassifier(self.image_labels)

    def __len__(self):
        return len(self.image_labels)

    def __getitem__(self, idx):
        img_path, label = self.image_labels[idx]
        image = Image.open(img_path).convert('RGB')
        if self.transform:
            image = self.transform(image)

        # 使用分类器对标签进行分类
        # label = self.classifier.classify(label)

        return image, label


if __name__ == '__main__':
    import time

    start = time.time()
    dataset = E3C(root_dir='./data/E3C', train=True, transform=default_transform)
    print(f'Time: {time.time() - start}')
    # 查看dataset的方法
    # print(dir(dataset))
    print(dataset[1][1])
    print(dataset.image_labels[0])
    # lower_bound: 4.167
    # upper_bound: 5.833
>>>>>>> Stashed changes
