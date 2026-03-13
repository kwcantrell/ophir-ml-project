#!/bin/sh
set -e

# NOTE: This script is deprecated.
# All installations are now done in Dockerfile.
# Run the Dockerfile build to install Ollama (as root).

echo "Installing Ollama..."
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model if specified
if [ -n "${MODEL}" ] && [ "${MODEL}" != "" ]; then
  echo "Pulling model: ${MODEL}"
  ollama serve &
  sleep 3
  ollama pull "${MODEL}"
fi

echo "Done installing Ollama."