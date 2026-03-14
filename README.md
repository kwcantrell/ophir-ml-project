# PyTorch ML Project

A production-ready PyTorch machine learning project template following industry best practices.

**Features:**
- Reproducible training with full seed control (Python, NumPy, PyTorch, CuDNN)
- Optimized DataLoader patterns with producer-consumer design
- Mixed precision (AMP) training support
- W&B experiment tracking integration
- TorchMetrics-based evaluation utilities
- Early stopping and checkpoint management
- Comprehensive linting with Ruff/Black/Mypy
- Pre-commit hooks for code quality enforcement

[View on GitHub](https://github.com/kwcantrell/ophir-ml-project) | [Documentation](docs/modules.md) | [Best Practices](docs/best-practices-guide.md)

---

## 📦 Project Overview

This repository provides a production-ready template for PyTorch machine learning projects:

**What's included:**
- **configs/** - YAML configuration files for training, evaluation, and inference
- **models/** - Pre-built model architectures (ResNet18)
- **src/train/** - Training loop implementations and utilities
- **src/eval/** - Evaluation pipeline logic
- **src/utils/** - Shared utilities (seeds, data loading, metrics, tracking, training helpers)
- **scripts/** - Shell scripts for common workflows
- **notebooks/** - Jupyter notebook templates
- **tests/** - Unit and integration test suites

**Use this template to:**
- Start new ML projects with best practices built-in
- Standardize your team's ML development workflow
- Share reproducible training pipelines with colleagues

---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop (for containerized environment)
- VS Code (recommended for Dev Containers)

### Step-by-Step Setup

1. **Clone and open in VS Code**
   ```bash
   git clone https://github.com/kwcantrell/ophir-ml-project.git
   cd ophir-ml-project
   code .
   ```

2. **Wait for Dev Container to build** (first run may take a few minutes)

3. **Start training!**
   ```bash
   # Train with default configuration
   uv run python -m src.train.main --config configs/train.yaml

   # Or use a custom config
   uv run python -m src.train.main --config configs/train-custom.yaml
   ```

### Quick Reference Commands

```bash
# Install dependencies
uv sync

# Run training
uv run python -m src.train.main --config configs/train.yaml

# Run evaluation
uv run python -m src.eval.run --config configs/eval.yaml

# View experiment logs (WandB)
wandb offlinelogs

# Run tests
uv run pytest tests/ -v --cov=src

# Format code (Black + Ruff)
pre-commit run --all-files

# Check types
uv run mypy src/ models/
```

---

## 🛠️ Tool Stack Overview

| Category | Recommendation | Description |
|----------|---------------|-------------|
| **Package Manager** | UV | Fast, PEP 621 compliant package management |
| **Linter** | Ruff | Fast Python linter with formatting support |
| **Formatter** | Black | Opinionated code formatter (line-length: 100) |
| **Type Checker** | MyPy | Static type checking for Python |
| **Test Runner** | pytest | Comprehensive test framework with coverage |
| **Tracking** | W&B | Experiment tracking and visualization |
| **Pre-commit** | pre-commit-hooks | Automated code quality checks |

### Development Workflow

1. **Install dependencies** with `uv sync` (uses uv.lock)
2. **Run pre-commit hooks** before commits: `pre-commit run --all-files`
3. **Format code** with Black and Ruff automatically via pre-commit
4. **Type check** with MyPy for production code
5. **Run tests** with pytest coverage reporting

### uv Commands Reference

```bash
# Sync dependencies (creates uv.lock)
uv sync

# Run a script without activating venv
uv run <command>

# Add/upgrade packages
uv add <package>
uv upgrade <package>

# Add dev dependency
uv add --dev pytest ruff mypy

# Freeze current environment to lock file
uv lock
```

---

## 🔒 Security & Best Practices

### Container Isolation
The agent runs in a Docker container separate from your host system. By default, it cannot access files outside the workspace or mounted directories.

### Selective File Access
Only specific folders are visible to the agent:
- `/home/vscode/.claude` - AI configuration and generated files (mounted)
- `~/.ollama` - Local AI models (mounted)

**Not accessible:** System configs (`/etc`), user downloads, credentials outside mounts, or any path you don't explicitly expose.

### Limited User Privileges
Claude Code is installed for the `vscode` user only (not root). Even if an agent runs system commands, it operates with limited privileges.

---

## 🧱 How It Works

### Docker Containerization
Docker packages applications with their dependencies into standardized units called **containers**.

**Key Benefits:**
- **Reproducibility** - Same code runs identically everywhere
- **Isolation** - Applications don't step on each other's dependencies
- **Clean Slate** - Stop and restart for a fresh workspace

See [Dockerfile](/.devcontainer/Dockerfile) for build instructions showing what's installed.

### Dev Containers
Dev Containers extend Docker by integrating directly with VS Code. When you open this folder:
1. A `Dockerfile` defines your container image
2. `.devcontainer/` configures VS Code integration
3. Your IDE runs inside the container with pre-installed tools

See [devcontainer.json](/.devcontainer/devcontainer.json) for mount configuration.

### Project Structure

```
ophir-ml-project/
├── configs/              # YAML configs (train, eval, inference)
├── models/               # Pre-built model architectures
├── src/                  # Source code
│   ├── train/           # Training loop and utilities
│   ├── eval/            # Evaluation pipeline
│   └── utils/           # Shared utilities
├── tests/                # Unit and integration tests
├── notebooks/            # Jupyter notebooks
├── scripts/              # Shell scripts for workflows
├── docs/                 # Documentation (modules, best practices)
├── pyproject.toml       # Project configuration with dependencies
├── .pre-commit-config.yaml  # Pre-commit hooks
└── README.md            # This file
```

---

## 📚 Configuration Details

### Dockerfile
See [/.devcontainer/Dockerfile](/.devcontainer/Dockerfile) for:
- Base system (Ubuntu)
- System dependencies (curl, zstd)
- Ollama installation
- Claude Code setup as vscode user

### devcontainer.json
See [/.devcontainer/devcontainer.json](/.devcontainer/devcontainer.json) for:
- Port forwarding (11434 for Ollama API)
- Mount configurations (`.claude`, `~/.ollama`)
- GPU support (`--gpus=all`)

---

## 🔍 Troubleshooting

### Ollama Not Responding
- Check if service is running: `ollama serve`
- Verify port 11434 is accessible in VS Code terminal

### Claude CLI Commands Not Found
- Run `which claude` or `claude --version` to verify installation

### Slow Container Build on First Run
- Normal on first run while Docker pulls the image from registry
- Subsequent builds are cached and fast

### Pre-commit Hooks Not Running
- Install hooks: `pre-commit install`
- Or run manually: `pre-commit run --all-files`

---

## ✅ Summary

This Dev Container workspace provides:
1. **Consistent AI development environment** - Same setup everywhere
2. **Local LLM capabilities** via Ollama for offline/privacy-focused work
3. **Secure CLI access** via Claude Code installed as limited user
4. **Portable configuration** via mount points that persist across sessions

Use it to:
- Develop AI applications with consistent tooling
- Test local LLM-based workflows without external APIs
- Share your environment with colleagues via git

---

## 🤖 Machine Learning Best Practices

This repository follows industry-standard best practices for building production-ready PyTorch machine learning applications.

### Overview

The best practices guide covers:
- **Project Structure** - Modular, configurable folder layout
- **Data Loading** - Optimized DataLoader patterns with producer-consumer design
- **Training Loops** - Mixed precision (AMP), early stopping, gradient clipping
- **Evaluation** - TorchMetrics integration, custom metric callbacks
- **Experiment Tracking** - W&B or MLflow integration for reproducibility
- **Configuration Management** - YAML configs with OmegaConf support

### Recommended Tool Stack

| Category | Recommendation | Alternative |
|----------|---------------|-------------|
| **Config** | OmegaConf + YAML | Dict/JSON configs |
| **Tracking** | W&B (primary) | MLflow, TensorBoard |
| **Metrics** | TorchMetrics | sklearn.metrics |
| **Deployment** | TorchScript / ONNX | PyTorchServe, FastAPI |

### Essential Code Patterns

```python
# 1. Reproducibility setup
from src.utils import set_seeds
set_seeds(seed=42)

# 2. Optimized DataLoader configuration
from torch.utils.data import DataLoader
from src.utils.data_loading import create_dataloader
train_loader = create_dataloader(
    train_dataset,
    batch_size=32, shuffle=True,
    num_workers=4, pin_memory=True, prefetch_factor=2,
    persistent_workers=True
)

# 3. Training loop with AMP and early stopping
from src.utils import EarlyStopping, setup_mixed_precision
scaler = setup_mixed_precision()
early_stopping = EarlyStopping(patience=5, min_delta=0.01)

for epoch in range(epochs):
    train_loss = train_epoch(model, train_loader, criterion, optimizer, scaler=scaler)
    val_loss, val_acc = validate(model, val_loader, criterion, scaler=scaler)

    if early_stopping(epoch, val_loss):
        break

    optimizer.step()
    lr_scheduler.step()
```

### Additional Resources

- [PyTorch Best Practices Guide](https://pytorch.org/tutorials/beginner/basics/notes.html)
- [PyTorch Lightning](https://pytorch-lightning.readthedocs.io/)
- [WandB Documentation](https://docs.wandb.ai/)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)

---

## 📦 Python Package Management with UV

This project uses **uv** for fast, reliable Python package management.

### What is uv?

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package manager and interpreter written in Rust (10x+ faster than pip). It supports PEP 621 `pyproject.toml` workflows natively.

### Quick Start with UV

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Navigate to project directory
cd /path/to/project

# Create virtual environment and sync dependencies
uv venv .venv && source .venv/bin/activate  # Linux/Mac
# or
uv venv .venv && .venv\Scripts\activate.bat   # Windows

# Sync all dependencies from pyproject.toml
uv sync

# Run any command with uv (auto-resolves dependencies)
uv run python -c "print('Hello!')"
```

### Modern `pyproject.toml` Workflow

This project uses PEP 621-style configuration:

**Install production dependencies:**
```bash
uv sync --frozen  # Uses uv.lock for reproducible builds
```

**Add a new package:**
```bash
uv add numpy pandas
```

**Add dev dependency:**
```bash
uv add --dev pytest ruff mypy
```

**Run tests without activating venv:**
```bash
uv run pytest tests/ -v --cov=src
```

### pyproject.toml Structure

The project uses modern PEP 621 syntax:

```toml
[project]
name = "ophir-ml-project"
dependencies = ["torch>=2.0", ...]
requires-python = ">=3.9"

[dependency-groups]
dev = [
    "pytest>=7.4",
    "mypy>=1.8",
]
```

This allows `uv sync` to resolve all dependencies automatically.

### Notes on Requirements.txt

For backwards compatibility, a `requirements.txt` file is provided. However:
- Use `uv sync` for development (resolves from pyproject.toml)
- Use `uv pip install -r requirements.txt` only when necessary
- The `pyproject.toml` + `uv.lock` combination provides better reproducibility

---

## 🔗 External Resources

- [Docker Docs](https://docs.docker.com/get-started/) - Learn about containerization
- [Dev Containers Docs](https://containers.dev/) - Standard for containerized development environments
- [Ollama Docs](https://ollama.ai/docs) - Run local LLM models
- [Claude Code Docs](https://claude.ai/) - AI assistant CLI features

---

[Security guidance](/.devcontainer/best-practices.md#security) for this environment is documented in the Dev Container best practices guide.
