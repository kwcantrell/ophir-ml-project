"""
ResNet-based model definitions.

Note: Training logic should be placed in separate modules (src/train/).
"""

import torch
import torch.nn as nn
from torchvision.models import resnet18, ResNet18_Weights


class ResNet18(nn.Module):
    """ResNet-18 for image classification."""

    def __init__(self, num_classes: int = 10, pretrained: bool = True):
        super().__init__()
        # Use pretrained backbone if available
        weights = ResNet18_Weights.DEFAULT if pretrained else None
        self.backbone = resnet18(weights=weights)
        self.backbone.fc = nn.Linear(self.backbone.fc.in_features, num_classes)

    def forward(self, x):
        return self.backbone(x)
