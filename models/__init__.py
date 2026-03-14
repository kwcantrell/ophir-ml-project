"""
Model definitions for PyTorch applications.

This module contains only model architectures - training logic should be in separate modules.
"""

from models.classifier import ClassificationHead
from models.resnet import ResNet18


__all__ = ["ResNet18", "ClassificationHead"]
