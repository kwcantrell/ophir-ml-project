FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install curl as root (needed for install scripts)
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama as root (install script runs as root)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Install uv for fast dependency management (~10-100x faster than pip)
# Uses official install script with automatic path setup
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Add HEALTHCHECK for container readiness verification
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:11434/ || exit 1

# Switch to vscode user and install tools here
USER vscode

# Install Claude Code and uv for vscode user only
RUN curl -fsSL https://claude.ai/install.sh | bash && \
    curl -LsSf https://astral.sh/uv/install.sh | sh && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
