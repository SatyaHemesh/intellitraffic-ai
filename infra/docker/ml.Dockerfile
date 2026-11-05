# infra/docker/ml.Dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install critical system libraries for OpenCV and Ultralytics
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install ML dependencies
COPY ml/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy ML pipeline and scripts
COPY ml/ ./ml/
COPY scripts/ ./scripts/

# Default command to run the pipeline demo
CMD ["python", "scripts/run_pipeline_demo.py", "--video", "data/sample_videos/test_traffic.mp4"]