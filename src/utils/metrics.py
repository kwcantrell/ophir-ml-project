"""
Model evaluation utilities using TorchMetrics.

Provides pre-built metrics and custom evaluators for classification, regression, etc.
"""

import torch
import torch.nn.functional as F
import torchmetrics
from torchmetrics import (
    Accuracy,
    ConfusionMatrix,
    F1Score,
    Precision,
    Recall,
)
from torchmetrics.regression import MeanAbsoluteError, MeanSquaredError


class CustomEvaluator:
    """
    Evaluates model predictions using multiple metrics.

    Supports classification and regression tasks with configurable metric types.
    """

    def __init__(
        self,
        task: str = "multiclass",
        num_classes: int = 10,
        threshold: float = 0.5,
        **kwargs: object,
    ):
        """
        Args:
            task: 'binary', 'multiclass', or 'multilabel' classification, or 'regression'
            num_classes: Number of classes for classification (ignored for regression)
            threshold: Classification threshold (default 0.5)
            **kwargs: Additional arguments passed to metrics constructors
        """
        self.task = task
        self.num_classes = num_classes
        self.threshold = threshold

        # Define metrics based on task type
        self.metrics = self._init_metrics()

    def _init_metrics(self) -> dict[str, torchmetrics.Metric]:
        """Initialize metrics for the given task."""
        if self.task == "binary":
            return {
                "accuracy": Accuracy(task="binary", **self._common_kwargs()),
                "precision": Precision(task="binary", threshold=self.threshold),
                "recall": Recall(task="binary", threshold=self.threshold),
                "f1_score": F1Score(task="binary", threshold=self.threshold),
            }
        if self.task == "multiclass":
            return {
                "accuracy": Accuracy(task="multiclass", num_classes=self.num_classes),
                "precision_macro": Precision(
                    task="multiclass", num_classes=self.num_classes, average="macro"
                ),
                "precision_micro": Precision(
                    task="multiclass", num_classes=self.num_classes, average="micro"
                ),
                "recall_macro": Recall(
                    task="multiclass", num_classes=self.num_classes, average="macro"
                ),
                "recall_micro": Recall(
                    task="multiclass", num_classes=self.num_classes, average="micro"
                ),
                "f1_macro": F1Score(
                    task="multiclass", num_classes=self.num_classes, average="macro"
                ),
                "confusion_matrix": ConfusionMatrix(
                    task="multiclass", num_classes=self.num_classes, ignore_index=-100
                ),
            }
        if self.task == "regression":
            return {
                "mse": MeanSquaredError(**self._common_kwargs()),
                "mae": MeanAbsoluteError(**self._common_kwargs()),
            }
        raise ValueError(
            "Unknown task type. Supported tasks: binary, multiclass, multilabel, regression"
        )

    def _common_kwargs(self) -> dict[str, object]:
        """Get common kwargs for all metrics."""
        return {"ndim": 1}

    @torch.no_grad()
    def evaluate(self, logits: torch.Tensor, labels: torch.Tensor) -> dict[str, float]:
        """
        Evaluate model predictions.

        Args:
            logits: Raw model outputs (unnormalized)
            labels: Ground truth labels

        Returns:
            Dictionary of metric names to values
        """
        # Normalize logits to probabilities if needed
        probs = torch.sigmoid(logits) if logits.shape[-1] == 2 else F.softmax(logits, dim=-1)

        preds = probs.argmax(dim=-1) if self.task != "binary" else (probs > self.threshold).float()

        # Reset all metrics
        for metric in self.metrics.values():
            metric.reset()

        # Update metrics with new predictions
        for metric in self.metrics.values():
            metric.update(preds, labels)

        # Compute and return results
        return {name: metric.compute().item() for name, metric in self.metrics.items()}


def evaluate_classification(
    logits: torch.Tensor | dict[str, torch.Tensor],
    labels: torch.Tensor,
    num_classes: int = 10,
) -> dict[str, float]:
    """
    Evaluate a classification model.

    Args:
        logits: Model outputs (raw predictions)
            Can be a dict for multi-label/multi-task models
        labels: Ground truth labels
        num_classes: Number of classes

    Returns:
        Dictionary of metric values
    """
    # Handle multi-task/multi-label input format
    if isinstance(logits, dict):
        all_preds = {}
        all_labels = []
        for task_name, task_logits in logits.items():
            preds = F.softmax(task_logits, dim=-1).argmax(dim=-1)
            all_preds[task_name] = preds
            all_labels.append(labels)

        evaluator = CustomEvaluator(task="multiclass", num_classes=num_classes)
        results = {}
        for task_name, preds in all_preds.items():
            metrics = evaluator.evaluate(preds, all_labels[0])
            for key, val in metrics.items():
                results[f"{task_name}_{key}"] = val
        return results

    # Single-label classification
    evaluator = CustomEvaluator(task="multiclass", num_classes=num_classes)
    return evaluator.evaluate(logits, labels)


def evaluate_regression(predictions: torch.Tensor, targets: torch.Tensor) -> dict[str, float]:
    """
    Evaluate a regression model.

    Args:
        predictions: Model predictions
        targets: Ground truth values

    Returns:
        Dictionary of metric values (MSE, MAE)
    """
    mse = MeanSquaredError().compute(predictions, targets).item()
    mae = MeanAbsoluteError().compute(predictions, targets).item()
    return {"mse": mse, "mae": mae}
