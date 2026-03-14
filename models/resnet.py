"""
ResNet-based model definitions.

Note: Training logic should be placed in separate modules (src/train/).
"""

import torch
import torch.nn as nn
from torchvision.models import ResNet18_Weights, resnet18


class ResNet18(nn.Module):
    """ResNet-18 for image classification."""

    def __init__(self, num_classes: int = 10, pretrained: bool = True) -> None:
        super().__init__()
        # Use pretrained backbone if available
        weights = ResNet18_Weights.DEFAULT if pretrained else None
        self.backbone = resnet18(weights=weights)
        self.backbone.fc = nn.Linear(self.backbone.fc.in_features, num_classes)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.backbone(x)  # type: ignore[no-any-return]
