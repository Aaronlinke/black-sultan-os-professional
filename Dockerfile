# Black Sultan OS - Production Dockerfile
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Node.js for frontend building
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs

# Copy Python requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy frontend source and build
COPY frontend/ ./frontend/
WORKDIR /app/frontend
RUN npm install && npm run build

# Copy backend source
WORKDIR /app
COPY src/ ./src/
COPY *.py ./

# Copy built frontend to static directory
RUN mkdir -p src/static && cp -r frontend/dist/* src/static/

# Create database directory
RUN mkdir -p src/database

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=src/main.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/api/health || exit 1

# Run the application
CMD ["python", "src/main.py"]
