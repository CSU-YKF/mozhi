from torch import nn
from torchvision.models import vit_b_16, resnet50

resnet = resnet50(weights=None, num_classes=1)
resnet.conv1 = nn.Conv2d(1, 64, kernel_size=7, stride=2, padding=3, bias=False)
vit = vit_b_16(weights=None, num_classes=1)
vit.conv_proj = nn.Conv2d(1, 768, kernel_size=(16, 16), stride=(16, 16))

