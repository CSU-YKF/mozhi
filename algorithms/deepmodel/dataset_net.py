import os
import shutil
from e3c import E3C  # 确保这里正确导入你的E3C类


def create_directories(base_path):
    # 创建三个分类的目录
    for i in range(3):
        dir_path = os.path.join(base_path, f'{i}')
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)


def restructure_dataset(dataset, base_path):
    for index, (img_path, label) in enumerate(dataset.image_labels):
        # 根据标签确定新的文件夹
        label = dataset[index][1]
        class_folder = f'{label}'
        new_path = os.path.join(base_path, class_folder, os.path.basename(img_path))

        # 复制文件到新的目录
        shutil.copy(img_path, new_path)


def main():
    root_dir = './data/E3C'  # 设置为你的原始数据集路径
    base_path = './data/E3C_Net'  # 设置为重构后的数据集路径

    # 创建目录结构
    # create_directories(base_path)

    # 为训练和测试数据集创建E3C实例
    train_dataset = E3C(root_dir, train=True)
    validation_dataset = E3C(root_dir, train=False)
    # 重构训练和测试数据集
    restructure_dataset(train_dataset, './data/E3C_Net/train')
    restructure_dataset(validation_dataset, './data/E3C_Net/validation')


if __name__ == '__main__':
    main()
