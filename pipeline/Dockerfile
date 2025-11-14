FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spacy model
RUN python -m spacy download en_core_web_sm

# Download NLTK data
RUN python -c "import nltk; nltk.download('stopwords')"

# Copy the pipeline code
COPY . .

# Create data directory
RUN mkdir -p /app/data

# Set environment variable for unbuffered output
ENV PYTHONUNBUFFERED=1

# Run the pipeline
CMD ["python", "main.py"]

