# Sử dụng Python 3.11 slim để tránh lỗi python-magic
FROM python:3.11-slim

# Cài system dependencies cần thiết
RUN apt-get update && apt-get install -y \
    tesseract-ocr \
    ghostscript \
    libmagic1 \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements trước (tăng cache layer)
COPY requirements.txt .

# Upgrade pip & install Python packages
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy toàn bộ project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port (Render default: 10000)
EXPOSE 10000

# Start server
CMD ["gunicorn", "ocrsite.wsgi", "--bind", "0.0.0.0:10000"]
