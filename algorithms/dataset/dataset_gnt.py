# Function: 读取gnt数据集
import struct
import numpy as np
from PIL import Image
import os
import torch.utils.data as data
from torchvision import transforms
#定义自己的数据集
class GNTDataset(data.Dataset):
    # root_dir: 数据集所在的根目录
    # transform: 数据转换
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.data_list = self.get_data_list()

    # 建立一个数据列表，方便返回索引和求数据集大小
    def get_data_list(self):
        data_list = []
        for dirpath, dirnames, filenames in os.walk(self.root_dir):
            for filename in filenames:
                if filename.endswith('.gnt'):
                    data_list.append(os.path.join(dirpath, filename))
        return data_list
    # 根据索引获取数据
    def __getitem__(self, index):
        file_path = self.data_list[index]
        img, label = self.load_data(file_path)
        if self.transform:
            img = self.transform(img)
        return img, label
    def __len__(self):
        return len(self.data_list)

    # 读取数据，为了返回索引
    def load_data(self, file_path):
        with open(file_path, 'rb') as f:
            # 读取头信息
            tagcode = struct.unpack('2B', f.read(2))[0]
            width = struct.unpack('2B', f.read(2))[0]
            height = struct.unpack('2B', f.read(2))[0]

            # 读取图片和标签
            img_raw= np.frombuffer(f.read(width * height), dtype=np.uint8)
            img = Image.fromarray(img_raw.reshape((height, width)))
            label = tagcode
        return img, label
#定义数据转换
data_transforms = transforms.Compose([
    transforms.RandomRotation(10),
    transforms.Resize((256, 256)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.5], std=[0.5])
])
#定义数据加载器
batchsize=64
train_dataset = GNTDataset(root_dir='Gnt1.0Train', transform=data_transforms)
train_loader = data.DataLoader(train_dataset, batch_size=batchsize, shuffle=True)
test_dataset = GNTDataset(root_dir='Gnt1.0Test', transform=data_transforms)
test_loader = data.DataLoader(test_dataset, batch_size=batchsize, shuffle=True)
#测试数据集
print(train_dataset[0])
print(train_dataset[0][0].size())
print(len(train_dataset))#训练数据集大小
print(len(test_dataset))#测试数据集大小
