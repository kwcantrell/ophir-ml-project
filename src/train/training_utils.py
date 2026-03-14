"""
Common training utilities including learning rate scheduling and callbacks.
"""

import torch


class LearningRateScheduler:
    """
    Wrapper for learning rate schedulers with epoch-based step control.

    Supports common schedulers like StepLR, MultiStepLR, CosineAnnealingLR.
    """

    def __init__(self, scheduler: torch.optim.lr_scheduler._LRScheduler):
        """Initialize with an existing PyTorch scheduler."""
        self.scheduler = scheduler

    def step(
        self,
        epoch: int,
        current_step: int | None = None,
    ) -> "LearningRateScheduler":
        """
        Step the scheduler.

        Args:
            epoch: Current epoch number
            current_step: Override internal step counter (optional)

        Returns:
            Self for method chaining
        """
        if self.scheduler.last_epoch != epoch and not isinstance(
            self.scheduler, torch.optim.lr_scheduler.ReduceLROnPlateau
        ):
            # Step based on epochs for periodic schedulers
            self.scheduler.step()
        return self

    def state_dict(self) -> dict:
        """Get scheduler state dictionary for saving."""
        return {
            "scheduler": self.scheduler.state_dict(),
            "epoch": self.scheduler.last_epoch,
        }

    def load_state_dict(self, state_dict: dict):
        """Load state dictionary to restore scheduler."""
        self.scheduler.load_state_dict(state_dict["scheduler"])


def get_lr_scheduler(
    optimizer: torch.optim.Optimizer,
    scheduler_type: str = "CosineAnnealingLR",
    **kwargs,
) -> LearningRateScheduler:
    """
    Create a learning rate scheduler.

    Args:
        optimizer: PyTorch optimizer
        scheduler_type: Type of scheduler ('CosineAnnealingLR', 'StepLR', etc.)
        **kwargs: Additional arguments for the scheduler

    Returns:
        LearningRateScheduler wrapper
    """
    # Map scheduler names to actual schedulers
    schedulers = {
        "cosine": torch.optim.lr_scheduler.CosineAnnealingLR,
        "cosine_annealing": torch.optim.lr_scheduler.CosineAnnealingLR,
        "linear": torch.optim.lr_scheduler.LinearLR,
        "step": torch.optim.lr_scheduler.StepLR,
        "multiplicative": torch.optim.lr_scheduler.MultiStepLR,
        "reduce_on_plateau": torch.optim.lr_scheduler.ReduceLROnPlateau,
    }

    scheduler_class = schedulers.get(scheduler_type, torch.optim.lr_scheduler.CosineAnnealingLR)
    new_scheduler = scheduler_class(
        optimizer,
        **kwargs,
    )
    return LearningRateScheduler(new_scheduler)
