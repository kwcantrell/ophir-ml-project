# AI Development Container Setup

This is a pre-configured development environment that gives AI agents safe access to tools for coding work. It uses Docker containers to create an isolated workspace, and Ollama for running local AI models without needing internet access.

**Ready to get started?** Open this folder in VS Code, wait for the container to build, and you're ready to use! For more details on how this works or security considerations, see the sections below.

---

## 🔍 What Is an AI Agent?

Before diving into technical details, it helps to understand what makes AI agents different from regular AI chatbots:

- **LLM (Large Language Model)** = Predictive text like autocomplete on steroids
  - Given input, predicts and generates the next word in a sequence
  - Can summarize, translate, write stories... but only with your explicit prompts

- **Agent** = LLM plus tools and decision-making
  - Uses an LLM as a "brain" to decide what actions to take
  - Can read files, run commands, query APIs, and iterate until a task is done
  - Manages its own memory and context between steps

**Think of it this way:** A chatbot answers questions. An agent completes tasks by taking action.

> **See more:** [How Tool Calling Works](#how-tool-calling-works-detail) - For understanding the agentic loop in detail

---

## 🛠️ Tools You Can Use

| Tool | What It Does | Why It Matters |
|------|--------------|----------------|
| **[Docker](#what-is-docker-containerization)** | Creates isolated containers | Agent stays safe; workspace resets cleanly each session |
| **[Dev Containers](#what-are-dev-containers-basics)** | VS Code integration for containers | Your IDE runs inside the container with all tools pre-installed |
| **[Ollama](#why-run-ollama-locally)** | Runs local AI models | No internet needed; private and reliable |
| **[Claude Code](https://claude.ai/)** | AI assistant CLI | Provides advanced coding help in your terminal |

All tools are installed automatically when the container builds. When you're done, just stop the container to reset everything cleanly.

> **See more:** [Security Overview](#security-overview) - Why access is limited and what files are visible to agents

---

## 🔄 The Agentic Loop in Action

Here's how an AI agent completes a task like "Read this file and explain it":

1. You provide a request: *"Read /path/to/file and summarize it"*
2. Agent interprets intent using its LLM "brain"
3. Agent calls the **Read tool** to fetch the file contents
4. LLM processes the information and plans next steps
5. Agent may call **Bash** or other tools to take actions
6. Loop continues until task is complete

### Why This Matters for Development

- **Tool calling** = The actual work done (reading code, running tests, fixing bugs)
- **Context window** = Working memory for what the agent currently knows
- **Agentic behavior** = Autonomous problem-solving with your approval

> **See more:** [How Tool Calling Works](#how-tool-calling-works-detail) - Deep dive into tool decision-making
> **See more:** [Agentic Patterns](#agentic-patterns-deep-dive) - Understanding behavioral patterns

---

## ⚠️ Safety First: How This Environment Protects You

AI agents can be powerful, but they also need access to do their work. This setup balances capability with safety:

### 1. Container Isolation
The agent runs in a Docker container separate from your host system. By default, it cannot access files outside the workspace or mounted directories.

### 2. Selective File Access
Only specific folders are visible to the agent:
- `/home/vscode/.claude` - AI configuration and generated files
- `~/.ollama` - Local AI models

**Not accessible:** System configs (`/etc`), user downloads, credentials outside mounts, or any path you don't explicitly expose.

### 3. Limited User Privileges
Claude Code is installed for the `vscode` user only (not root). Even if an agent runs system commands, it operates with limited privileges.

> **See more:** [Security Deep Dive](#security-deep-dive) - Detailed security rationale and threat mitigations
> **See more:** [Mount Configuration](/.devcontainer/devcontainer.json) - Technical mount specifications

---

## 🧱 How This Environment Works

### What is Docker? (Basic Concept)

Docker packages applications with their dependencies into standardized units called **containers**.

**Analogy:** Think of containers like shipping containers for software. Just as physical containers can hold goods from different manufacturers on a single ship without conflict, containers let multiple applications run side-by-side on one machine without conflicts.

**Key Benefits:**
- **Reproducibility** - Same code runs identically everywhere (dev → staging → prod)
- **Isolation** - Applications don't step on each other's dependencies
- **Clean Slate** - Stop and restart for a fresh workspace

> **See more:** [Docker Deep Dive](#what-is-docker-containerization) - Technical details about containers

### What are Dev Containers?

Dev Containers extend Docker by integrating directly with VS Code. When you open a folder marked as a Dev Container, VS Code automatically opens inside the containerized environment.

**How it works:**
1. A `Dockerfile` defines your container image
2. `.devcontainer/` configures VS Code integration
3. Your IDE runs inside the container with pre-installed tools

> **See more:** [Dev Containers Deep Dive](#what-are-dev-containers-basics) - Technical details and benefits

### Why Run Ollama Locally?

Ollama is a lightweight runtime for local AI models. It lets Claude Code use models without internet access.

**Why local matters:**
- **Privacy** - Models never leave your machine
- **Offline capability** - Work continues when internet is unavailable
- **Performance** - No network latency waiting for external APIs

> **See more:** [Ollama Setup Details](#why-run-ollama-locally-detail) - Model options and configuration

---

## 🚀 Getting Started

Follow these steps to set up your AI development environment:

1. **Install Docker Desktop** (if not already installed on your system)
   - Download from https://www.docker.com/products/docker-desktop/

2. **Open this folder in VS Code**
   - The Dev Container will automatically build and install tools
   - Wait for the progress indicator to complete (first run takes a few minutes)

3. **(Optional) Pull Ollama models**
   ```bash
   ollama pull llama3.2
   ```
   This downloads local AI models. You only need to do this once.

4. **Start using!**
   - Run `ollama serve` in the VS Code terminal (or leave it running)
   - Use the `claude` command or `/claude` slash command for AI assistance

That's it! Your environment is now ready for AI-powered development.

> **See more:** [Understanding Containerization](#what-is-docker-containerization) - How containers create isolated workspaces
> **See more:** [Security Design Decisions](#security-deep-dive) - Why this setup is safe

---

## 📚 Optional Deep Dives

These sections provide technical background for those who want to understand the underlying systems. You can skip these if you just want to use the tools.

---

## 🔍 How Tool Calling Works (Detail)

The agentic loop I described earlier involves several moving parts. Here's a deeper look:

### The Context Window

Every tool interaction uses a "context window" - essentially the agent's working memory for that turn:

- **System prompt**: Pre-loaded instructions about tools and safety
- **User messages**: Your requests and questions
- **Tool responses**: Outputs from Read, Bash, WebFetch, etc.
- **LLM responses**: The agent's thinking and planning

**Why it matters:**
- Too much context → LLM loses focus ("needle in a haystack" problem)
- Strategic memory (e.g., `.claude` mount) persists between sessions
- Tools provide fresh information to keep context lean

### Why Context Management Matters

| Session Progress | Context State | Risk |
|------------------|---------------|------|
| Turn 1-5: Few file reads | ~50KB context | Clean, focused reasoning |
| Turn 50+ files read | 500KB+ context | Slower, potential hallucinations |
| Unbounded reads | Context overflow | Agent loses track of goal |

**Best practice:** Ask agents to read specific files one at a time rather than "read all files."

> **See more:** [Context Window Management](#context-window-basics) - Managing memory limits effectively

---

## 🧱 How Tool Calling Can Be Risky (Detail)

Unbounded tool access creates real risks. Here's why this setup mitigates them:

### File System Clutter Prevention
When an agent repeatedly reads files:
- Disk usage grows with every read
- Context window fills with unrelated data
- Agent performance degrades as context approaches limits (8K–128K tokens)

**This setup:** Mounts only specific directories, preventing unbounded file access.

### Security Risk Mitigation

| Risk | How This Setup Protects You |
|------|---------------------------|
| **Directory Traversal** | Agent can only read mounted paths (`.claude`, `~/.ollama`) |
| **Host File Access** | Container isolation blocks access to `/etc`, `/var`, user files outside mounts |
| **Privilege Escalation** | Claude installed as `vscode` user, not root |
| **Credential Exposure** | Sensitive files (`.env`, keys) excluded from mounts by default |
| **Context Injection** | Strategic memory in `.claude` mount, not workspace clutter |

### Without These Safeguards

If agents had unrestricted access:
- Could read any file on your system
- Would see all past conversations and files you've opened
- Could theoretically execute arbitrary code or exfiltrate data
- Context would bloat with every tool call made

**This is why minimal necessary access matters:** It enables productive automation while keeping your host system secure.

> **See more:** [Security Rationale](#security-deep-dive) - Complete security design explanation

---

## 🧱 What is Docker? (Containerization Deep Dive)

### Basic Concept

A Docker container packages an application with:
- Its code
- All dependencies (libraries, system tools)
- Configuration files
- A defined runtime environment

**Analogy:** Think of containers like virtual machines that are much lighter and faster to start. Unlike VMs which include a full guest operating system, containers share the host's kernel but run in isolated process spaces.

### How Docker Helps Agents

**1. File System Clutter Prevention**
- Container has its own filesystem state
- Deleting container removes all temporary/intermediate files
- Prevents workspace pollution from failed installs or experimental code

**2. Context Window Protection**
- Agent operates in bounded environment (only mounted paths visible)
- Reduces "needle in haystack" problem by limiting filesystem scope
- Faster tool responses with smaller, focused search space

**3. Security Risk Containment**
- If agent generates malicious code or runs dangerous commands, they're sandboxed
- Host system remains protected even if container is compromised

> **See more:** [Dockerfile](/.devcontainer/Dockerfile) - Build instructions showing what's installed

### Container Lifecycle

**When you start the container:**
1. Docker builds from `Dockerfile` (cached, fast after first run)
2. Installs system dependencies (curl, zstd, utilities)
3. Installs Ollama as root for local model inference
4. Switches to `vscode` user for Claude Code installation

**When you stop the container:**
1. All processes halt (Ollama not running)
2. Workspace resets (any files agent created are gone)
3. Your config persists via mount points if mounted

**When you restart:**
- Image is already cached locally → Fast startup
- Model cache preserved → No re-downloading models
- Mounts restore your `.claude` config and Ollama models

> **Why stop containers?** To reset context and prevent bloat. You're not losing anything permanent—just clearing the agent's working space.

---

## 🧱 What are Dev Containers? (Dev Container Deep Dive)

### How They Work

1. **Dockerfile** - Defines your container image
   - Base system (Ubuntu in this case)
   - System dependencies (curl, zstd)
   - Application tools (Ollama, Claude Code)

2. **.devcontainer/** - VS Code integration config
   - `devcontainer.json` specifies mounts and settings
   - Mount points bind your local paths to container paths
   - Port forwarding configured for Ollama's 11434

### Benefits for Agent Workflows

**1. Context Consistency**
- Same environment for every session
- Mount points provide persistent `.claude` state
- Models cached locally at fixed location

**2. Multi-Agent Safety**
- Share workspace with colleagues? Each runs in their own container
- Agent experiments don't affect host system
- Can switch between different tool configurations (Python vs Node, etc.)

**3. Performance Optimization**
- Fresh container = clean slate each session
- No accumulated file clutter from previous work
- Fast file access via bind-mounts (zero-copy)

> **See more:** [devcontainer.json](/.devcontainer/devcontainer.json) - Full configuration specification

### Container vs. Virtual Environment

| Aspect | Virtual Environment | Dev Container |
|--------|--------------------|---------------|
| **Isolation** | Shares host filesystem | True filesystem isolation |
| **Dependencies** | Installed on host machine | Packaged in image |
| **Portability** | Machine-specific | Git-reproducible anywhere |
| **Team Sharing** | Each member installs manually | Share git repo, everyone gets same env |

Dev containers are overkill for simple Python projects but excel for AI/ML work where consistent tooling matters.

---

## 🧱 Why Run Ollama Locally? (Detail)

### What is Ollama?

Ollama is a minimal runtime for local LLMs. Think of it like Docker, but for running large language models locally.

**What it provides:**
- Model management (pull, run, delete)
- HTTP API for client applications
- Native inference on your hardware (CPU or GPU)

### Local vs. Cloud Models

| Factor | Cloud API | Local Ollama |
|--------|-----------|---------------|
| **Cost** | Pay per token | Free (uses your hardware) |
| **Privacy** | Data sent to vendor | Stays on your machine |
| **Offline** | Needs internet | Works without connection |
| **Latency** | Network-dependent | Local speed (~10-30 tokens/s) |
| **Quotas** | Subject to rate limits | Unlimited |

### Model Management

```bash
# Pull a model (downloads to ~/.ollama/)
ollama pull llama3.2

# Run with default parameters
ollama run llama3.2

# View running models
ollama list

# Remove unused models
ollama rm llama3.2

# Keep server running in background
ollama serve &
```

> **Note:** The container includes Ollama installation but leaves model pulling to you for manual control over resources and privacy.

> **See more:** [Features README](/.devcontainer/features/README.md) - Why devcontainer features were removed

---

## 🔍 Context Window Management (Best Practices)

### Understanding the Limits

The context window is effectively the agent's short-term memory:
- **System prompt**: Instructions and tool descriptions (~1KB)
- **Your conversation**: Questions and tool responses
- **Tool history**: All reads, writes, commands executed

**Why limits matter:**
- Contexts up to 128K tokens are common but not magic
- Every token counts toward the limit
- Too much irrelevant data → LLM loses focus on key details ("needle in haystack")

### Best Practices

**1. Be Specific with Requests**
```
Instead of: "Analyze my entire codebase"
Use: "Read src/auth.py and explain the auth flow"
```

**2. Delete Intermediate Files**
If an agent creates temporary files during work, delete them when done to prevent clutter bloat.

**3. Use Strategic Memory**
- Store reusable configs in `.claude` mount (persists across sessions)
- Keep workspace clean for focused context
- Don't accumulate temporary files indefinitely

---

## 🔍 Agentic Patterns (Deep Dive)

### Single-shot Tasks
One tool call completes the task: "Read this file" → Done. Most simple operations fall here.

### Multi-step Chains
Sequential tool calls: "Search API → Parse results → Summarize findings." Each response feeds the next prompt.

### Looped Operations
Repeat until success: "Retry failed API call up to 3× before reporting error."

### Conditional Branching
Decision-based actions: "If file doesn't exist, create it with default template instead."

> **See more:** [Agentic Loop Example](#the-agentic-loop-in-action) - Practical walkthrough with step-by-step detail

---

## 🧱 Security Deep Dive

### Why User-Level Installation?

The Dockerfile installs Ollama as root (required for system setup) but then switches to `vscode` user to install Claude Code. This provides:

1. **Least Privilege:** Only the VS Code user can use Claude CLI
2. **Audit Trail:** Easy to see what's installed for which user
3. **Containment:** Even if compromised, agent can't access root-level resources

### How Each Layer Protects You

| Layer | What It Blocks | Real-World Example |
|-------|----------------|--------------------|
| **Docker isolation** | Host filesystem access | Agent can't read `/etc/passwd` or your personal files outside mounts |
| **User-level install** | System commands as root | `bash -c whoami` returns `vscode`, not `root` |
| **Selective mounts** | Sensitive data exposure | No accidental reads of `.env`, SSH keys, or credentials |
| **Bind mount constraints** | Directory traversal | Agent confined to `/workspace` subdirs + selected paths only |

### When You Stop the Container

Stopping the container does NOT mean deleting your work:
- ✅ Ollama models stay cached in `~/.ollama` (mounted)
- ✅ Claude config stays in `.claude` (mounted)
- ✅ Workspace files remain on disk
- ✅ Docker image is cached for fast restart

But it **does** mean:
- ❌ Agent processes stop (Ollama not running)
- ❌ Agent's working context clears (no accumulated files from tool calls)
- ❌ Any temporary state agent created disappears

**This is intentional:** Resetting the agent's "working memory" prevents context bloat while preserving what you care about.

---

## 🔍 Troubleshooting Tips

### Ollama Not Responding
- Check if service is running: `ollama serve &`
- Verify port 11434 is accessible in VS Code terminal

### Claude CLI Commands Not Found
- Restart container (tools need fresh install as vscode user)
- Run `which claude` or `claude --version` to verify installation

### Slow Container Build on First Run
- This is normal for first run as Docker pulls the image from registry
- Subsequent builds are cached and much faster
- Consider pulling Ollama models in parallel: `ollama pull llama3.2:parallel=4`

---

## ✅ Summary

This Dev Container workspace provides:
1. **Consistent AI development environment** - Same setup everywhere you share the repo
2. **Local LLM capabilities** via Ollama for offline/privacy-focused work
3. **Secure CLI access** via Claude Code installed as limited user
4. **Portable configuration** via mount points that persist across sessions

### How This Setup Helps Agents Succeed

| Challenge | Solution | Benefit |
|-----------|----------|---------|
| Context drift from file clutter | Selective mounts (`.claude`, `~/.ollama` only) | Clean workspace, focused reasoning |
| Host system compromise | Container isolation + user-level install | Security even if agent misbehaves |
| Slow repeated downloads | Cached Docker image + model cache | Fast subsequent sessions |
| Agent losing track in large trees | Bounded filesystem scope | Faster tool calls, less hallucination |

Use it to:
- Develop AI applications with consistent tooling
- Test local LLM-based workflows without external APIs
- Share your environment with colleagues via git

**Need more info?** Check the official docs linked throughout this README.

---

## 🔗 External Resources

- **Docker Docs:** https://docs.docker.com/
- **Dev Containers:** https://containers.dev/
- **Ollama:** https://ollama.com/docs
- **Claude AI:** https://claude.ai/
