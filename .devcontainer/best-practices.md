# Best Practices Guide

This guide covers recommended workflows and important considerations for using this AI Development Container environment.

---

## 📦 Build Context Optimization

### Use a `.dockerignore` File

The repository includes a `.dockerignore` at the project root (`/.dockerignore`) with comprehensive exclusions. This file prevents unnecessary files like `node_modules`, `__pycache__`, `.git/`, and IDE folders from being sent to Docker builds, reducing build time and image size.

**Current exclusions include:**
```
.git/
.env*
node_modules/
.idea/
.vscode/
.pytest_cache/
.docker/
models/
```

For new projects, copy this file or create your own with similar exclusions.

### Dockerfile Recommendations

Current Dockerfile structure is well-optimized:
- ✅ Uses minimal base image (Ubuntu)
- ✅ Installs packages as root, then switches to vscode user
- ✅ Only essential packages installed (curl, zstd)
- ✅ Includes HEALTHCHECK for container readiness verification

**Note on HEALTHCHECK:** The current implementation uses `curl -f http://localhost:11434/` which checks port availability. Avoid API-specific paths like `/api/tags` as they may not be available on Ollama startup.

```dockerfile
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:11434/ || exit 1
```

---

## 🔐 Mount Configuration Best Practices

### Current Mount Strategy

The `.devcontainer/devcontainer.json` uses bind mounts for:
- `/workspace/.claude` → AI configuration and memory
- `~/.ollama` → Model cache

**This is intentional:** Minimal access, no host credential exposure.

### What NOT to Mount (Common Mistakes)

| Don't Mount | Why |
|------------|-----|
| `./src` or subdirs | Workspace should be git-tracked; avoid accidental commit of work-in-progress |
| `~/.ssh/` | SSH keys outside container exposure risk |
| `~/.config/*` | User-specific configs not needed in container |
| Environment variables files (`.env`) | Unless explicitly managed, credentials get exposed |

### Recommended Mount Pattern

```jsonc
// .devcontainer/devcontainer.json - mount only what's necessary
{
  "name": "AI Development Container",

  // Persistent state: AI config + model cache
  "mounts": [
    {
      "type": "bind",
      "source": "/workspace/.claude",
      "target": "/home/vscode/.claude"
    },
    {
      "type": "bind",
      "source": "~/.ollama",
      "target": "/home/vscode/.ollama"
    }
  ],

  // Recommended: Add .dockerignore at repo root
  "dockerfile": "../.devcontainer/Dockerfile"
}
```

---

## 🛡️ Security Design Decisions

### Why User-Level Claude Code Installation?

| Concern | Mitigation |
|---------|------------|
| Agent runs system commands | Installed as vscode user, not root |
| Container is shared/collaborative | Least privilege principle enforced |
| Compromise scenario | Host filesystem isolated via Docker |
| Sensitive data exposure | Only specified paths mounted |

### What Gets Access Inside Container?

**Allowed:**
- ✅ `.claude` workspace (your AI config)
- ✅ `~/.ollama` model cache
- ✅ Workspace files in `.devcontainer/` root
- ✅ Mounted directories (explicitly configured)

**Blocked by default:**
- ❌ `/etc/*` - System configuration
- ❌ `/var/*` - Logs and services
- ❌ `~/.ssh/*` - Unless explicitly mounted
- ❌ `~/.aws/*`, `~/.gitconfig` - Unless mounted
- ❌ Any path outside mounted directories

### Security Checklist Before Sharing Repo

- [x] `.dockerignore` exists at project root - excludes build artifacts, node_modules, IDE folders
- [x] No `.env` or credential files committed to repo (except managed credentials)
- [x] Workspace doesn't contain sensitive data (keys, passwords)
- [x] README documents security considerations and mount strategy
- [x] `.gitignore` configured to prevent accidental commits of work-in-progress

---

## 🔄 Container Lifecycle Management

### When to Stop vs. Delete

| Action | When | What Persists |
|--------|------|---------------|
| **Stop** (`Ctrl+C`) | Session end, break time | Models, config, workspace files |
| **Rebuild** (reload) | Fresh start after changes | Models, config; new install as vscode user |
| **Delete Container** | Debugging, reset agent state | Docker image remains cached |
| **Remove Image** | Clean install from scratch | Everything gone (re-downloads on rebuild) |

### Recommended Workflow

```bash
# First time: Build container
vscode reload

# Pull models once
ollama pull llama3.2

# Stop when done for session
# Next VS Code reload will restart fresh

# If agent creates clutter, stop and rebuild once
docker volume prune --filter label=com.docker.compose.project=devcontainer  # optional cleanup
```

### Why Containers Feel "Stateless"

- ✅ Agent's working context resets on each stop/restart
- ✅ Workspace files persist (mounted)
- ✅ Model cache persists (`~/.ollama` mounted)
- ⚠️ Agent-created intermediate files do NOT persist

---

## 🗝️ Handling Secrets and Credentials

### Never Store Credentials in Workspace

**CRITICAL:** Never store secrets (API keys, passwords, tokens) directly in your workspace folder or git repository. These will be exposed to the container.

### Standard Practices for Secret Management

**Use mounted secret files (if absolutely necessary):**
```jsonc
// devcontainer.json - mount a secure secret location
{
  "mounts": [
    {
      "type": "bind",
      "source": "${localEnv:HOME}/.config/secrets",
      "target": "/home/vscode/.config/secrets"
    }
  ]
}
```

**Recommended alternatives:**
- Use environment variables set in your shell (not committed to repo)
- Use Docker secrets for swarm mode (if applicable)
- Use secret management tools (Vault, AWS Secrets Manager, etc.)
- Pass credentials via CI/CD pipeline at build time

### Detecting Secret Exposure

Before committing code, run these checks:
```bash
# Check for common secret patterns in git history
git log -p --all | grep -iE "(password|secret|api_key|token)"

# Check current .env files before commit
find . -name ".env*" -exec cat {} \; 2>/dev/null
```

**If secrets are detected:**
1. Remove from workspace
2. Add to `.gitignore` if applicable
3. Rotate any exposed credentials immediately

---

## 📚 Development Workflow Tips

### 1. Pull Models Strategically

```bash
# Interactive selection (recommended for first-time users)
ollama serve
# Then in new terminal:
ollama pull llama3.2

# Parallel download for large models
ollama pull llama3.2:parallel=4

# Multiple models for different tasks
ollama pull llama3.1:8b          # General purpose
ollama pull codellama            # Coding assistant
ollama pull tinyllama:1.1         # Small, fast for quick answers
```

### 2. Use Strategic Memory Files

Store reusable configs in `.claude/`:

```bash
# ~/.claude/config.json - Your personal settings
{
  "model": "llama3.2",
  "tools": ["read", "bash", "web-fetch"],
  "custom_instructions": "Always consider security implications..."
}
```

### 3. Clear Context When Needed

If agent behavior degrades or context bloats:

```bash
# Stop container to reset agent state
docker stop ai-dev-container

# Rebuild once (keeps models and config)
vscode reload

# Delete image if starting completely fresh
docker rmi ai-dev-image
```

---

## 🔧 Troubleshooting Best Practices

### Claude Code Not Found After Rebuild

```bash
# Verify installation path
which claude

# Expected: /home/vscode/.local/bin/claude or similar

# If not found, rebuild container (one-time install needed)
docker stop <container>
docker rm <container>
docker rmi <image>  # Optional: remove image to force re-download
```

### Ollama Connection Issues

```bash
# Check if service is running
ollama list
ollama serve &

# Verify port forwarding (devcontainer.json)
# Port 11434 should be accessible in VS Code terminal
```

---

## 📖 Feature Scripts Deprecation Status

**The `.devcontainer/features/` directory has been deprecated.** All installations are now done in the Dockerfile:

- ✅ Ollama: Installed as root via install script (line 10 of Dockerfile)
- ✅ Claude Code: Installs as vscode user on container rebuild (line 20)

**Why removed:**
- Simplifies builds with single source of truth
- Avoids feature dependency issues
- User-level installs for better security (vs root)

**Migration from features-based setup:**
1. Your existing `devcontainer.json` still works without changes
2. Ollama needs to be started manually (`ollama serve &`) before first use
3. Claude Code auto-installs on container rebuild; no action needed

---

## 🎯 Quick Reference

| Task | Command |
|------|---------|
| Start container | Open folder in VS Code, wait for build |
| Pull models | `ollama pull <model-name>` |
| Start Ollama | `ollama serve &` |
| Reset agent state | Stop + reload VS Code |
| View running models | `ollama list` |
| Delete model | `ollama rm <model-name>` |

---

## 📞 Need Help?

- **Read this file first:** This best practices guide covers most scenarios
- **Check security deep dive:** See the main README's "Security Deep Dive" section
- **Review Dockerfile:** Understand what gets installed and why
- **Inspect mounts:** Read `.devcontainer/devcontainer.json` for mount configuration

---

*Last updated: 2024*