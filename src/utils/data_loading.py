"""
Data loading utilities with optimized DataLoaders.

Implements producer-consumer pattern for optimal GPU utilization.
"""

import torch
from torch.utils.data import DataLoader


def create_dataloader(
    dataset,
    batch_size: int = 32,
    shuffle: bool = False,
    num_workers: int = 0,
    pin_memory: bool = True,
    prefetch_factor: int = 2,
    persistent_workers: bool = False,
    **kwargs,
) -> DataLoader:
    """
    Create an optimized DataLoader with producer-consumer pattern.

    The producer-consumer pattern uses multiple workers to pre-process batches
    before they're consumed by the GPU, maximizing pipeline utilization.

    Args:
        dataset: PyTorch Dataset object
        batch_size: Number of samples per batch
        shuffle: Whether to shuffle training data
        num_workers: Number of parallel data loading workers
        pin_memory: Pin memory for faster CUDA transfers (if using GPU)
        prefetch_factor: Number of batches to load in advance
            - 0: no prefetching (single consumer)
            - >1: producer-consumer pattern with prefetch buffer
        persistent_workers: Keep workers alive between epochs
        **kwargs: Additional arguments passed to DataLoader

    Returns:
        Optimized DataLoader instance
    """
    return DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        pin_memory=pin_memory,
        prefetch_factor=prefetch_factor,
        persistent_workers=persistent_workers,
        **kwargs,
    )


def get_optimal_num_workers(num_cpus: int = None) -> int:
    """
    Get optimal number of workers based on CPU availability.

    Args:
        num_cpus: Number of CPU cores (defaults to torch.get_num_threads())

    Returns:
        Recommended number of workers for DataLoader
    """
    if num_cpus is None:
        num_cpus = torch.get_num_threads()
    # Limit workers based on system RAM and CPU count
    # Generally: 0 workers on Windows/Mac, up to 8-16 on Linux with 32GB+ RAM
    import sys

    if sys.platform.startswith("win"):
        return 0
    if num_cpus < 4:
        return min(1, max(0, num_cpus - 1))
    return min(4, max(0, num_cpus // 2))
