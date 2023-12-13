import numpy as np
from timm.models import vision_transformer
import torch.nn as nn
import torch


mean=[0.6710, 0.6657, 0.6493]
std=[0.2706, 0.2712, 0.2746]
mean = np.mean(mean)
std = np.mean(std)
print(mean, std)
