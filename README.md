# AI Setup Dev Container

This is a pre-configured development environment that gives AI agents safe access to tools like file reading, web fetching, and bash commands.

---

## 🛠️ Tools Available

| Tool | Purpose |
|------|---------|
| **[Docker](#dev-container-setup)** | Creates isolated containers for safe agent execution |
| **[Dev Containers](#dev-containers)** | VS Code integration - IDE runs inside container |
| **[Ollama](#ollama-configuration)** | Runs local LLM models (port 11434) |
| **[Claude Code](https://claude.ai/)** | AI assistant CLI for terminal assistance |

All tools are installed automatically when the container builds. When you're done, just stop the container to reset everything cleanly.

---

## 🔒 Security Overview

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

### Ollama Configuration
Ollama is a lightweight runtime for local LLM models on port 11434.

**Why local matters:**
- **Privacy** - Models never leave your machine
- **Offline capability** - Work continues without internet
- **Performance** - No network latency to external APIs

To use Ollama, run `ollama serve` in the VS Code terminal first (or leave it running). Then pull models with:

```bash
ollama pull llama3.2
```

---

## 🚀 Getting Started

1. **Install Docker Desktop** (if not already installed)
   - Download from https://www.docker.com/products/docker-desktop/

2. **Open this folder in VS Code**
   - The Dev Container will automatically build and install tools
   - First run takes a few minutes; subsequent runs use cached image

3. **(Optional) Pull Ollama models**
   ```bash
   ollama pull llama3.2
   ```
   Only needed once. Run `ollama serve` in terminal to keep it running.

4. **Start using!**
   - Use the `claude` command or `/claude` slash command for AI assistance

That's it! Your environment is now ready for AI-powered development.

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

## 🔗 External Resources

- [Docker Docs](https://docs.docker.com/get-started/) - Learn about containerization
- [Dev Containers Docs](https://containers.dev/) - Standard for containerized development environments
- [Ollama Docs](https://ollama.ai/docs) - Run local LLM models
- [Claude Code Docs](https://claude.ai/) - AI assistant CLI features

---

## 🔐 Security Notes

This environment prioritizes your security through:
- **Container isolation** - Agents run in sandboxed environment
- **Limited user privileges** - Claude Code installed as vscode user, not root
- **Selective mounts** - Only necessary directories exposed
- **Bind mount constraints** - Agents confined to workspace + selected paths

For detailed security rationale and threat mitigations, see [.devcontainer/best-practices.md](.devcontainer/best-practices.md).

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
|----------|---------------|-----|--|
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

### Resources

- [PyTorch Best Practices Guide](https://pytorch.org/tutorials/beginner/basics/notes.html)
- [PyTorch Lightning](https://pytorch-lightning.readthedocs.io/)
- [WandB Documentation](https://docs.wandb.ai/)
- [MLflow Tracking](https://mlflow.org/docs/latest/tracking.html)

---

## 📦 Python Package Management with UV

This project uses **uv** for fast, reliable Python package management.

### What is uv?

[uv](https://github.com/astral-sh/uv) is an extremely fast Python package manager and interpreter written in Rust. It's up to 10x faster than pip/virtualenv.

### Quick Start with UV

```bash
# Install uv if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv .venv

# Activate the environment
source .venv/bin/activate  # On Linux/Mac
# or
.venv\Scripts\activate.bat  # On Windows

# Install dependencies from requirements.txt
uv pip install -r requirements.txt

# Or add packages interactively
uv pip install torch torchvision torchaudio
```

### uv Commands Cheat Sheet

```bash
# Create new project with template
uv init <project-name> --python 3.10

# Sync project (installs dependencies)
uv sync

# Run Python script with uv
uv run python my_script.py

# Add dev dependencies
uv add torch torchvision

# Run without activating venv
uv run pytest tests/

# Show dependency tree
uv pip tree --graph | dot -Tpng > deps.png

# Check for updates
uv self update
```

### Requirements File

The `requirements.txt` file in the project root contains production dependencies. Use it with:

```bash
# Install from requirements
uv pip install -r requirements.txt

# Or use uv pip directly
uv pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
```

---
