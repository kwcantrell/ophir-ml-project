"""Utility modules for PyTorch applications."""

# Note: These imports use relative paths to avoid mypy duplicate module errors.
# When this package is installed, these will import correctly from the installed location.
try:
    from .data_loading import create_dataloader, get_optimal_num_workers  # noqa: F401
    from .experiment_tracking import WandBLogger, setup_experiment_tracking  # noqa: F401
    from .metrics import CustomEvaluator, evaluate_classification, evaluate_regression  # noqa: F401
    from .seeds import set_determinism, set_seeds  # noqa: F401
    from .training import (  # noqa: F401
        EarlyStopping,
        save_checkpoint,
        setup_mixed_precision,
    )
except ImportError:
    # This can happen during development or CI when not using installed package.
    # These imports are ignored in those contexts.
    pass


__all__ = [
    "create_dataloader",
    "get_optimal_num_workers",
    "WandBLogger",
    "setup_experiment_tracking",
    "CustomEvaluator",
    "evaluate_classification",
    "evaluate_regression",
    "set_seeds",
    "set_determinism",
    "EarlyStopping",
    "save_checkpoint",
    "setup_mixed_precision",
]
