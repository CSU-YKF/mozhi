import torch
import torchvision
import numpy as np
import pickle

with open('../dataset/HWDB/mapping.pkl', 'rb') as f:
    mapping = pickle.load(f)
num_classes = len(mapping['index_to_code'])
index_to_code = mapping['index_to_code']

# Create the model and load the weights
model = torchvision.models.resnet152(weights=None, num_classes=num_classes)
model.conv1 = torch.nn.Conv2d(1, 64, kernel_size=(7, 7), stride=(2, 2), padding=(3, 3), bias=False)
model.load_state_dict(torch.load('runs/HWDB_experiment/resnet154/final_model.pth'))


def transform_image(image):
    """
    Transform the image to the format expected by the model.
    """
    transform = torchvision.transforms.Compose([
        torchvision.transforms.ToPILImage(),
        torchvision.transforms.Resize((168, 168)),
        torchvision.transforms.ToTensor(),
    ])
    return transform(image)


def predict_top3(model, image, device, index_to_code):
    """
    Predict the top 3 most likely classes for the input image.
    """
    # Transform and add a batch dimension ([1, C, H, W])
    image = transform_image(image).unsqueeze(0).to(device)

    # Set the model to evaluation mode
    model.eval()

    # No need to track gradients for inference
    with torch.no_grad():
        outputs = model(image)
        # Get the top 3 predictions
        _, indices = torch.topk(outputs, 3)
        top3_indices = indices[0].tolist()

    # Convert indices to actual GBK codes
    top3_codes = [index_to_code[idx] for idx in top3_indices]

    return top3_codes


# Example usage:
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)
# Load an image of handwritten Chinese character
# image = ...
# top3_predictions = predict_top3(model, image, device, index_to_code)
# print("Top 3 predictions:", top3_predictions)
