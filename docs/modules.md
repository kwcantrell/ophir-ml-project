# Module Documentation

## `src/utils/seeds.py`

**Purpose:** Reproducibility utilities for setting random seeds.

**Key Functions:**
- `set_seeds(seed)` - Sets seeds for Python, NumPy, and PyTorch
- `set_determinism(algorithm, seed)` - Also sets CuDNN deterministic mode

**Usage Example:**
```python
from src.utils import set_seeds

set_seeds(seed=42)  # Full reproducibility
```

---

## `src/utils/data_loading.py`

**Purpose:** Optimized DataLoader configuration with producer-consumer pattern.

**Key Functions:**
- `create_dataloader(dataset, batch_size, ...)` - Create DataLoader with optimal settings
- `get_optimal_num_workers(num_cpus)` - Get recommended worker count

**Recommended Parameters:**
```python
train_loader = create_dataloader(
    dataset,
    batch_size=32,
    num_workers=4,
    pin_memory=True,
    prefetch_factor=2,
    persistent_workers=True,  # For multi-epoch training
)
```

---

## `src/utils/experiment_tracking.py`

**Purpose:** W&B experiment tracking integration.

**Key Classes:**
- `WandBLogger` - Logging wrapper for metrics, images, artifacts
- `setup_experiment_tracking(config)` - Auto-setup from config

**Usage Example:**
```python
from src.utils import WandBLogger

logger = WandBLogger(project_name="my-project", entity="your-org")

# Log metrics
logger.log_metrics({"loss": 0.5, "acc": 0.75}, step=epoch)
logger.save_artifact("models/best.pth", name="best-model")
```

---

## `src/utils/metrics.py`

**Purpose:** TorchMetrics-based evaluation utilities.

**Key Classes:**
- `CustomEvaluator` - Multi-metric evaluator for classification/regression

**Usage Example:**
```python
from src.utils import CustomEvaluator, evaluate_classification

# Classification
evaluator = CustomEvaluator(task="multiclass", num_classes=10)
metrics = evaluator.evaluate(logits, labels)  # Returns dict of metric values

# Or use convenience function
results = evaluate_classification(logits, labels, num_classes=10)
```

---

## `src/utils/training.py`

**Purpose:** Training utilities including early stopping and checkpoint management.

**Key Classes/Functions:**
- `EarlyStopping(patience, min_delta)` - Early stopping callback
- `save_checkpoint(model, optimizer, ...)` - Save model with metadata
- `setup_mixed_precision()` - Setup GradScaler for AMP training

**Usage Example:**
```python
from src.utils import EarlyStopping, save_checkpoint, setup_mixed_precision

early_stop = EarlyStopping(patience=5, min_delta=0.01)
scaler = setup_mixed_precision()  # Returns GradScaler or None

# In training loop
if early_stop(epoch, val_loss):
    break

save_checkpoint(model, optimizer, scaler=scaler, epoch=epoch, metric=val_loss)
```

---

## `src/train/training_loop.py`

**Purpose:** Standard training and validation functions.

**Key Functions:**
- `train_epoch(model, dataloader, criterion, optimizer, ...)` - Train one epoch
- `validate(model, dataloader, criterion)` - Compute validation metrics

**Usage Example:**
```python
from src.train import train_epoch, validate

# Training loop
scaler = setup_mixed_precision()
for epoch in range(num_epochs):
    train_loss, _ = train_epoch(
        model=model,
        dataloader=train_loader,
        criterion=criterion,
        optimizer=optimizer,
        device=device,
        scaler=scaler,
        lr_scheduler=lr_scheduler,
        epoch_progress_callback=lambda idx, tot, loss: print(
            f"Step {idx}/{tot}, loss={loss:.4f}"
        ),
    )
    val_loss, val_acc = validate(model, val_loader, criterion)
```

---

## `src/train/training_utils.py`

**Purpose:** Learning rate scheduling utilities.

**Key Classes:**
- `LearningRateScheduler` - Wrapper for epoch-based scheduler stepping
- `get_lr_scheduler(optimizer, scheduler_type)` - Factory function

**Supported Schedulers:**
- `cosine` / `cosine_annealing` - Cosine annealing with warm restarts
- `linear` - Linear warmup schedule
- `step` / `multiplicative` - Step-based or decay schedulers

---

## `src/utils/__init__.py`

**Purpose:** Exposes all utilities for easy import.

**Import Example:**
```python
from src.utils import (
    set_seeds,
    create_dataloader,
    WandBLogger,
    CustomEvaluator,
    EarlyStopping,
    save_checkpoint,
    setup_mixed_precision,
)
```

---

## `models/resnet.py`

**Purpose:** Predefined model architectures (ResNet variants).

**Usage Example:**
```python
from models import ResNet18

model = ResNet18(num_classes=10, pretrained=True)
model.eval()
```

---

## `configs/*.yaml`

**Purpose:** Configuration files for different training scenarios.

| File | Description |
|------|-------------|
| `train.yaml` | Training configuration with model, data, and hyperparameters |
| `eval.yaml` | Evaluation pipeline configuration |
| `inference.yaml` | Deployment/inference settings |
