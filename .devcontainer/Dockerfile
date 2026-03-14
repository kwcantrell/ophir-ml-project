FROM mcr.microsoft.com/devcontainers/base:ubuntu

# Install curl and Python as root (needed for install scripts and Python projects)
RUN apt-get update && apt-get install -y \
    curl \
    zstd \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install uv to /usr/local so all users can access it
RUN curl -LsSf https://astral.sh/uv/install.sh | UV_INSTALL_DIR=/usr/local/bin sh
ENV PATH="/root/.local/bin:${PATH}"

# Install Ollama for local AI development
RUN curl -fsSL https://ollama.com/install.sh | sh

# Switch to vscode user and install tools here
USER vscode

# Set up uv venv with correct ownership
RUN uv venv /home/vscode/.venv && \
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && \
    echo 'source /home/vscode/.venv/bin/activate' >> ~/.bashrc

# Install Claude Code and bootstrap uv's virtual environment
RUN curl -fsSL https://claude.ai/install.sh | bash


# Add HEALTHCHECK to verify Claude Code is available (not Ollama)
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
  CMD curl -f http://localhost:11434/ || exit 1
