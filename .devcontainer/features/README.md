# Feature Scripts Directory - DEPRECATED

**This directory is deprecated but kept for reference.** All installations are now done in the Dockerfile.

## Why were features moved to Dockerfile?

| Reason | Benefit |
|--------|---------|
| **Consistency** | No feature loading issues or dependency conflicts across different host environments |
| **Security** | Claude Code installs as vscode user only (not system-wide root) |
| **Simplicity** | Single Dockerfile is the single source of truth for what gets installed |
| **Manual Control** | Users decide when to start Ollama service rather than auto-starting at install |

## What this means for you:

### If you're **using** this devcontainer template:
- ✅ The Dockerfile has already been updated - just use it as-is
- 📦 Ollama is installed (as root) and ready to pull models
- 🔐 Claude Code will be installed when the container is rebuilt for your user

### If you're **migrating** from old feature-based setup:
1. Your existing `.devcontainer/devcontainer.json` configuration still works
2. You can now use `--update-content` flag for fresh installs
3. Optional: Rebuild container once to ensure Claude Code installs for your user

### Starting Ollama (recommended workflow):

```bash
# Option 1: Interactive model selection (first time)
ollama serve
# Then pull desired models in a new terminal
ollama pull llama3

# Option 2: Pull and run in one command
ollama pull llama3:latest && ollama serve &
```

## About the feature scripts in this directory:

The `install.sh` and `devcontainer-feature.json` files are kept for documentation purposes only. They reflect the old devcontainer features format which is no longer used in this repository.

## Troubleshooting

**"Ollama not found after rebuild"** - Run `ollama serve` manually or pull a model to start the service.

**"Claude Code plugin errors"** - Rebuild the container once after your initial setup to install Claude Code for your user account.
