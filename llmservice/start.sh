#!/bin/bash

set -e

echo "[🔧] Starting environment setup..."

if [[ -n "$ROOT_DIR" ]]; then
    echo "[🔧] Using ROOT_DIR: $ROOT_DIR"
    ROOT_DIR=$(realpath "$ROOT_DIR")
    WORKDIR="$ROOT_DIR/llmservice"
else
    echo "[🔧] Using default ROOT_DIR: /workspace"
    ROOT_DIR="/workspace"
    WORKDIR="/workspace/llmservice"
fi

# Force reinstall Flask and Blinker to bypass distutils conflict
pip install --upgrade pip
pip install --ignore-installed --force-reinstall flask blinker

# Install project dependencies
pip install --no-cache-dir -r $WORKDIR/requirements.txt

# Authenticate with Hugging Face
if [[ -n "$HF_TOKEN" ]]; then
    echo "[🔐] Logging in to Hugging Face..."
    python -c "from huggingface_hub import login; login('$HF_TOKEN')"
fi

# Launch Flask app
echo "[🚀] Starting app..."
cd $WORKDIR
# warn viewer that downloading and building the model will take time...
echo "[⏳] Downloading and building the model may take a while. Please be patient."
python app/main.py
