FROM nvidia/cuda:12.1.0-runtime-ubuntu22.04

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    git \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
RUN pip3 install --no-cache-dir \
    runpod \
    marker-pdf \
    torch \
    torchvision \
    Pillow

# Copy handler
COPY handler.py /app/handler.py

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV TORCH_HOME=/runpod-volume/.cache/torch
ENV HF_HOME=/runpod-volume/.cache/huggingface

# Models will be downloaded on first run and cached in /runpod-volume
# This is faster than downloading during build

# Run the handler
CMD ["python3", "-u", "handler.py"]
