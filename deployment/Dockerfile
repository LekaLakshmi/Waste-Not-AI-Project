# Use a lightweight Python base image
FROM python:3.10-slim

# Prevent Python from writing .pyc files & enable unbuffered logs
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements first (so Docker can cache layers)
COPY requirements.txt .

# Install system dependencies needed for Pillow & TensorFlow
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg62-turbo-dev \
    zlib1g-dev \
    libssl-dev \
    libaio-dev \
    && rm -rf /var/lib/apt/lists/*


# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy your full app into the container
COPY . .

# Expose Gradio app port & Prometheus metrics port
EXPOSE 7860
EXPOSE 8000

# Run the WasteNot application
CMD ["python", "app.py"]
