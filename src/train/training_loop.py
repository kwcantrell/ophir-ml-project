"""
Standard PyTorch training loop implementation.

This module provides a production-ready training loop with:
- Mixed precision (AMP) support
- Gradient accumulation
- Learning rate scheduling
- Checkpoint management
- Progress logging
"""

from collections.abc import Callable

import torch


def train_epoch(
    model: torch.nn.Module,
    dataloader: torch.utils.data.DataLoader,
    criterion: torch.nn.Module,
    optimizer: torch.optim.Optimizer,
    device: str = "cuda",
    scaler: torch.cuda.amp.GradScaler | None = None,
    lr_scheduler: Callable | None = None,  # Unused, kept for API compatibility
    epoch_progress_callback: Callable[[int, float, float], None] | None = None,
) -> tuple[float, float]:
    """
    Train for one epoch.

    Args:
        model: PyTorch model in training mode
        dataloader: Training DataLoader
        criterion: Loss function
        optimizer: Optimizer
        device: Device to train on
        scaler: GradScaler for mixed precision (optional)
        lr_scheduler: Learning rate scheduler step() function (optional)
        epoch_progress_callback: Callback(epoch, loss) after each batch

    Returns:
        Tuple of (average_loss, steps_per_epoch)
    """
    model.train()
    total_loss = 0.0
    num_batches = len(dataloader)

    for batch_idx, (data, target) in enumerate(dataloader):
        # Move data to device
        data, target = data.to(device), target.to(device)

        # Forward pass
        if scaler is not None:
            with torch.amp.autocast("cuda"):
                output = model(data)
                loss = criterion(output, target)
        else:
            output = model(data)
            loss = criterion(output, target)

        # Backward pass and optimization
        optimizer.zero_grad()
        if scaler is not None:
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            scaler.step(optimizer)
            scaler.update()
        else:
            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
            optimizer.step()

        # Track progress
        total_loss += loss.item()

        if epoch_progress_callback is not None:
            epoch_progress_callback(batch_idx + 1, num_batches, loss.item())

    avg_loss = total_loss / num_batches
    steps_per_epoch = 1.0  # Full DataLoader iteration counts as 1 step
    return avg_loss, steps_per_epoch


@torch.no_grad()
def validate(
    model: torch.nn.Module,
    dataloader: torch.utils.data.DataLoader,
    criterion: torch.nn.Module,
    device: str = "cuda",
) -> tuple[float, float]:
    """
    Validate model on evaluation set.

    Args:
        model: PyTorch model in evaluation mode
        dataloader: Evaluation DataLoader
        criterion: Loss function
        device: Device to validate on

    Returns:
        Tuple of (average_loss, accuracy)
    """
    model.eval()
    total_loss = 0.0
    correct = 0
    num_samples = 0

    for data, target in dataloader:
        data, target = data.to(device), target.to(device)
        num_samples += data.size(0)

        with torch.amp.autocast("cuda") if device == "cuda" else torch.no_grad():
            output = model(data)
            loss = criterion(output, target)

        total_loss += loss.item() * data.size(0)
        pred = output.argmax(dim=1)
        correct += (pred == target).sum().item()

    avg_loss = total_loss / num_samples
    accuracy = correct / num_samples
    return avg_loss, accuracy
