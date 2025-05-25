FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install system dependencies, including OpenJDK
RUN apt-get update && apt-get install -y \
    openjdk-17-jre-headless \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    libssl-dev \
    libffi-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set JAVA_HOME environment variable (optional but good practice)
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
ENV PATH="$JAVA_HOME/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Expose the port your app runs on
EXPOSE 8000

# Start the app (replace with your actual entry point if different)
# CMD ["waitress-serve", "--port=8000", "app:app"]

# Run with Gunicorn (adjust app module as needed)
CMD ["gunicorn", "--workers=2", "--bind=0.0.0.0:${PORT:-8000}", "app:app"]
