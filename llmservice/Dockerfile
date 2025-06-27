# Use official PyTorch runtime with CUDA support
FROM pytorch/pytorch:2.2.2-cuda12.1-cudnn8-runtime

# Create work directory
WORKDIR /workspace

# Set environment variables for non-interactive installs
ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    ffmpeg \
    libsndfile1 \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and install Python deps early to leverage caching
COPY requirements.txt ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy app code (or use git clone in start.sh if pulling live)
COPY . /workspace

# Make the startup script executable
RUN chmod +x /workspace/start.sh

# Expose Flask port
EXPOSE 5000

# Run the app
CMD ["bash", "/workspace/start.sh"]
