import os
import numpy as np
import torch
from PIL import Image

from .e3c import default_transform
from .vig import cgnn_model


def load_model(model, model_weights):
    """
    加载训练好的模型
    """
    model.load_state_dict(torch.load(model_weights, map_location="cuda" if torch.cuda.is_available() else "cpu"))
    model.to('cuda' if torch.cuda.is_available() else 'cpu')
    model.eval()  # 将模型设置为评估模式
    return model


def preprocess_image(image):
    """
    对图像进行预处理
    """
    transform = default_transform

    # 判断image是否为文件路径，或者是否已经被Image.open()打开
    if isinstance(image, str):
        image = Image.open(image).convert('RGB')
    elif not isinstance(image, Image.Image):
        raise ValueError('image参数必须是文件路径或者PIL.Image.Image对象')
    image = transform(image)
    image = image.unsqueeze(0)  # 增加批次维度
    return image


def infer(model, image):
    """
    使用模型进行推理
    """
    with torch.no_grad():
        outputs = model(image)
        return outputs


def gnn_score(image_path):
    """
    主函数，加载模型并对图像进行推理
    """
    # 从当前目录中的saved_models文件夹中加载模型CGNN.pth
    model_path = os.path.join(os.path.dirname(__file__), 'saved_models/CGNN.pth')
    model = load_model(cgnn_model, model_path).to('cuda' if torch.cuda.is_available() else 'cpu')
    image = preprocess_image(image_path).to('cuda' if torch.cuda.is_available() else 'cpu')
    prediction = infer(model, image)
    print(f'Predicted: {prediction.item()}')

    score = prediction.item()

    score += 2.5
    if score > 9:
        score = 9 - np.random.normal(0.5, 0.5)
    elif score < 1:
        score = 1 + np.random.normal(0.5, 0.5)

    # 保留score为一位小数
    score = round(score, 1)

    return float(score)


if __name__ == '__main__':
    predict = gnn_score('img.png')
    print(predict)
