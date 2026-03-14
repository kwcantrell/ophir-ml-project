"""
Model definitions for PyTorch applications.

This module contains only model architectures.
Training logic should be in separate modules.
"""

# Note: To use utilities from src.utils, import them directly from src.utils.*
# or set up proper relative imports after the package is installed.

# Example usage (when using the package as a local development setup):
# from utils.data_loading import (
#     create_dataloader,
#     get_optimal_num_workers,
# )
# from utils.experiment_tracking import (
#     WandBLogger,
#     setup_experiment_tracking,
# )

from models.resnet import ResNet18


__all__ = ["ResNet18"]
