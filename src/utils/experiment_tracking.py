"""
Experiment tracking integration with Weights & Biases (W&B).

Provides automatic logging for metrics, images, hyperparameters, and checkpoints.
"""

import os
from typing import Optional


try:
    import wandb
except ImportError:
    wandb = None


class WandBLogger:
    """Weights & Biases experiment logger."""

    def __init__(
        self, project_name: str, entity: str = None, name: str = None, notes: str = None, **kwargs
    ):
        """
        Args:
            project_name: W&B project name
            entity: W&B entity (organization/user), defaults to env var or GCP_GITHUB_USER
            name: Run name (optional, auto-generated if not provided)
            notes: Custom run notes (shows in sidebar)
            **kwargs: Additional arguments passed to wandb.init()
        """
        self.project_name = project_name
        self.entity = entity
        self.name = name
        self.notes = notes
        self.wandb_run = None

        # Initialize W&B if credentials are available
        if wandb is not None:
            try:
                self._init_wandb(**kwargs)
            except Exception as e:
                print(f"WandB logging disabled: {e}")

    def _init_wandb(self, **kwargs) -> "WandBLogger":
        """Initialize W&B run."""
        # Skip if running in CI or no API key found
        env_vars = ["WANDB_DISABLED", "WANDB_MODE"]
        if any(os.environ.get(v) for v in env_vars):
            return self

        self.wandb_run = wandb.init(
            project=self.project_name,
            entity=self.entity,
            name=self.name,
            notes=self.notes,
            config=kwargs.pop("config", {}),
            **kwargs,
        )
        return self

    def log_metrics(self, metrics: dict, step: int = None) -> "WandBLogger":
        """
        Log metrics to W&B.

        Args:
            metrics: Dictionary of metric names to values
            step: Optional step number for X-axis (defaults to epoch)

        Returns:
            Self for method chaining
        """
        if self.wandb_run is not None:
            self.wandb_run.log(metrics, step=step)
        return self

    def log_image(self, name: str, image: dict, step: int = None) -> "WandBLogger":
        """
        Log an image to W&B.

        Args:
            name: Image key/name
            image: Dictionary with keys 'caption' (optional) and 'bytes' or 'base64'
            step: Optional step number

        Returns:
            Self for method chaining
        """
        if self.wandb_run is not None:
            self.wandb_run.log({name: image}, step=step)
        return self

    def log_table(self, name: str, dataframe=None, data=None):
        """Log a table to W&B."""
        if self.wandb_run is not None and wandb is not None:
            self.wandb_run.log({name: wandb.Table(dataframe=dataframe, data=data)})
        return self

    def save_artifact(self, artifact_path: str, name: str = None) -> "WandBLogger":
        """
        Save a file/artifact to W&B.

        Args:
            artifact_path: Local path to artifact
            name: Artifact name (defaults to basename of path)

        Returns:
            Self for method chaining
        """
        if self.wandb_run is not None and wandb is not None:
            artifact = wandb.Artifact(name or os.path.basename(artifact_path))
            artifact.add_file(artifact_path)
            self.wandb_run.log_artifact(artifact)
        return self

    def finish(self):
        """Finish the current run."""
        if self.wandb_run is not None:
            self.wandb_run.finish()


def setup_experiment_tracking(config, **kwargs) -> Optional[WandBLogger]:
    """
    Set up experiment tracking based on configuration.

    Args:
        config: Configuration object or dict with 'experiment_tracking' section
        **kwargs: Additional arguments passed to WandBLogger

    Returns:
        WandBLogger instance if enabled and configured successfully, None otherwise
    """
    tracking = config.get("experiment_tracking", {})
    if not tracking.get("enabled", False):
        return None

    project_name = tracking.get("project_name", "pytorch-experiments")
    entity = tracking.get("entity", os.environ.get("WANDB_ENTITY"))

    return WandBLogger(project_name=project_name, entity=entity, **kwargs)
