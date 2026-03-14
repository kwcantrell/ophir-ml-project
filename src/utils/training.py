"""
Training loop utilities with early stopping, AMP, gradient clipping, etc.
"""

from datetime import datetime, timezone
import os
from typing import Optional

import torch


class EarlyStopping:
    """Early stopping to prevent overfitting."""

    def __init__(
        self,
        patience: int = 5,
        min_delta: float = 0.01,
        better_than_last_metric: bool = True,
        mode: str = "min",  # 'min' for loss, 'max' for accuracy
    ) -> None:
        """
        Args:
            patience: Number of epochs to wait before stopping
            min_delta: Minimum improvement required to reset patience counter
            better_than_last_metric: Stop if metric is worse than best seen (disabled by default)
            mode: 'min' to stop when loss stops decreasing, 'max' for accuracy
        """
        self.patience = patience
        self.min_delta = min_delta
        self.better_than_last_metric = better_than_last_metric
        self.mode = mode

        self.best_metric = float("inf") if mode == "min" else -float("inf")
        self.counter = 0
        self.stopped_epoch = None

    def __call__(self, epoch: int, metric: float) -> bool:
        """
        Check if early stopping should trigger.

        Args:
            epoch: Current epoch number
            metric: Metric value (lower is better for 'min' mode, higher for 'max')

        Returns:
            True if training should stop early
        """
        self.counter += 1

        # Update best metric if improved
        improved = False
        if self.mode == "min":
            if metric < self.best_metric - self.min_delta:
                self.best_metric = metric
                improved = True
            elif metric > self.best_metric and self.better_than_last_metric:
                return True  # Stopped because metric is worse than best seen
        else:  # 'max' mode
            if metric > self.best_metric + self.min_delta:
                self.best_metric = metric
                improved = True

        if improved:
            self.counter = 0
        elif self.counter >= self.patience:
            self.stopped_epoch = epoch
            print(
                f"Early stopping triggered at epoch {epoch}. "
                f"Best metric was {self.best_metric:.4f}."
            )
            return True

        return False

    def reset(self):
        """Reset early stopping state."""
        self.counter = 0
        self.stopped_epoch = None


def save_checkpoint(
    model,
    optimizer=None,
    scaler=None,
    epoch: int = None,
    metric: float = None,
    filepath: str = "checkpoints/checkpoint.pth",
):
    """
    Save a checkpoint with metadata.

    Args:
        model: PyTorch model to save
        optimizer: Optimizer (optional)
        scaler: GradScaler for AMP (optional)
        epoch: Current epoch number
        metric: Best metric value (e.g., validation loss)
        filepath: Path to save checkpoint
    """
    state_dict = {
        "epoch": epoch,
        "metric": metric,
        "model_state_dict": model.state_dict(),
        "optimizer_state_dict": optimizer.state_dict() if optimizer else None,
        "scaler_state_dict": scaler.state_dict() if scaler else None,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    # Ensure checkpoint directory exists
    os.makedirs(os.path.dirname(filepath), exist_ok=True)

    torch.save(state_dict, filepath)
    print(f"Checkpoint saved to {filepath}")
    return filepath


def setup_mixed_precision() -> Optional[torch.cuda.amp.GradScaler]:
    """
    Setup mixed precision training with GradScaler.

    Returns:
        GradScaler instance (or None if CUDA not available)
    """
    if torch.cuda.is_available():
        scaler = torch.cuda.amp.GradScaler(enabled=True)
        print("Mixed precision training enabled")
        return scaler
    print("CUDA not available, using standard precision")
    return None
