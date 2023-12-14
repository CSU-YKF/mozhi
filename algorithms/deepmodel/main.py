import torch
import torchvision.transforms as transforms
from PIL import Image

from .models import resnet, vit
from .e3c import default_transform


def load_model(model, model_weights):
    """
    加载训练好的模型
    """
    model.load_state_dict(torch.load(model_weights))
    model.eval()  # 将模型设置为评估模式
    return model


def preprocess_image(image):
    """
    对图像进行预处理
    """
    transform = default_transform
    if isinstance(image, str):
        image = Image.open(image).convert('RGB')
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


def main(image_path):
    """
    主函数，加载模型并对图像进行推理
    """
    model = load_model(resnet, './deepmodel/resnet50.pth')
    image = preprocess_image(image_path)
    prediction = infer(model, image)
    print(f'Predicted: {prediction.item()}')
    return prediction.item()


if __name__ == '__main__':
    predict = main('../utils/single_pre/li_with_grid.png')
