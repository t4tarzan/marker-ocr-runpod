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

# Pre-download Marker models to reduce cold start time
RUN python3 -c "from marker.models import load_all_models; load_all_models()"

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run the handler
CMD ["python3", "-u", "handler.py"]
