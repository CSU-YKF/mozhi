# Desc: 读取png格式的数据集
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
import os
from PIL import Image

class ChineseCharacterDataset(Dataset):
    def __init__(self, root_dir, transform=None):
        self.root_dir = root_dir
        self.transform = transform
        self.images = []
        self.labels = []
        for sub_dir in os.listdir(self.root_dir):
            sub_path = os.path.join(self.root_dir, sub_dir)
            if not os.path.isdir(sub_path):
                continue
            for img_name in os.listdir(sub_path):
                img_path = os.path.join(sub_path, img_name)
                self.images.append(img_path)
                self.labels.append(sub_dir)

    def __len__(self):
        return len(self.images)

    def __getitem__(self, idx):
        image = Image.open(self.images[idx]).convert('RGB')
        label = self.labels[idx] # 标签为文件夹名
        if self.transform:
            image = self.transform(image)
        return image, label

# 图像预处理方式
transform = transforms.Compose([
    # 将图像缩放到 224x224
    transforms.Resize((224, 224)),
    # 将图像转为 PyTorch Tensor
    transforms.ToTensor(),
    # 对图像进行标准化处理
    transforms.Normalize(mean=[0.5, 0.5, 0.5], std=[0.5, 0.5, 0.5])
])

# 加载数据集，并进行数据预处理
train_dataset = ChineseCharacterDataset(root_dir='./png_data/train', transform=transform)
test_dataset = ChineseCharacterDataset(root_dir='./png_data/test', transform=transform)

# 划分训练集和验证集，并封装为DataLoader类型
batch_size = 64
train_dataloader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True)
test_dataloader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

# 输出一张经过预处理后的图片
image, label = train_dataset[0]
print(image)
print(image.shape) # 输出形状为 torch.Size([3, 224, 224]) 的张量
print(label) # 输出对应的标签