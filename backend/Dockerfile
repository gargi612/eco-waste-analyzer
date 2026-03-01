# Use official Python 3.10 runtime as parent image
FROM python:3.10-slim

# Set working directory in container
WORKDIR /app

# Install system dependencies required for PyTorch and OpenCV (if needed)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first to leverage Docker cache
COPY requirements.txt .

# Install dependencies (CPU-only PyTorch is heavily recommended for Render to save space/memory)
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Copy the rest of the application code
COPY . .

# Expose port (Render dynamically assigns $PORT, but we expose 8000 for standard documentation)
EXPOSE 8000

# Run FastAPI app with Uvicorn
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
