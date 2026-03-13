# Feature Scripts Directory

This directory was formerly used for devcontainer features, but has been deprecated.

## Why removed?

All feature installations have been moved to the Dockerfile for:

1. **Consistency** - No feature loading issues or dependency conflicts
2. **Security** - Claude Code installs for vscode user only (not system-wide root)
3. **Simplicity** - Single Dockerfile as single source of truth
4. **Manual Control** - Users decide when to start Ollama service

## Install commands now in Dockerfile:

- **Ollama**: `curl -fsSL https://ollama.com/install.sh | sh` (runs as root)
- **Claude Code**: `curl -fsSL https://claude.ai/install.sh | bash` (runs as vscode user)

## Starting Ollama manually:

```bash
ollama serve              # Start the server
ollama pull <model-name>  # Pull models
```
