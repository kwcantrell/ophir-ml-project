"""
Reproducibility utilities for PyTorch training.

Ensure deterministic behavior across training runs by setting seeds and enabling
deterministic algorithms.
"""

import random

import numpy as np
import torch


def set_seeds(seed: int = 42) -> None:
    """
    Set all random seeds for reproducibility.

    Args:
        seed: Random seed value to use (default: 42).
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed(seed)
        torch.cuda.manual_seed_all(seed)
    # Enable deterministic algorithms
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False  # Disable for reproducibility


def set_determinism(algorithm: str = "cudnn", seed: int = 42) -> None:
    """
    Set CuDNN algorithm to the specified type.

    Args:
        algorithm: 'default', 'deterministic', or 'enabled' (alias for deterministic).
        seed: Random seed value to use (default: 42).
    """
    if algorithm in ("deterministic", "enabled"):
        torch.backends.cudnn.deterministic = True
    else:
        torch.backends.cudnn.benchmark = True

    set_seeds(seed)


# Convenience alias
set_determinism = set_determinism
