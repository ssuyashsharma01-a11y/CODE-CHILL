# Use Python 3.10 Slim - Balance between size and compatibility
FROM python:3.10-slim

# Set environment variables for Python stability
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# Global path injection to recognize 'app' inside 'backend'
ENV PYTHONPATH=/app/backend

# Working directory inside the sovereign container
WORKDIR /app

# ⚡ Install High-Performance System Dependencies
# Updated package names for compatibility with newer Debian/Slim images
RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev \
    gfortran \
    libopenblas-dev \
    liblapack-dev \
    libatlas3-base \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (Identity Cache Optimization)
COPY requirements.txt .

# Install dependencies (Caching this heavy step)
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Inject the entire project matrix into the image
COPY . .

# Sovereign Identity Port
EXPOSE 8000

# 🚦 Final Executive Command
# Using --app-dir backend to map the internal app structure correctly
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "backend", "--workers", "1"]