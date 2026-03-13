FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install curl as root (needed for install scripts)
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    && rm -rf /var/lib/apt/lists/*

# Stay as root for system package installations (Ollama)
USER root

# Install Ollama as root
RUN curl -fsSL https://ollama.com/install.sh | sh

# Switch to vscode user and install Claude Code here
USER vscode

# Install Claude Code for vscode user only
RUN curl -fsSL https://claude.ai/install.sh | bash
