# Use a Debian Bullseye–based Python 3.12 slim image.
FROM python:3.12-slim-bullseye

# Prevent Python from writing pyc files and enable unbuffered output.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies including build tools, ODBC libraries, and prerequisites.
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    gcc \
    libffi-dev \
    libssl-dev \
    unixodbc-dev \
    unixodbc \
    libodbc1 \
    gnupg2 \
    apt-transport-https \
    python3-pip \
    nginx \
    supervisor && \
    rm -rf /var/lib/apt/lists/*

# Add Microsoft repository and install the ODBC driver for SQL Server.
RUN curl -sSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > /etc/apt/trusted.gpg.d/microsoft.gpg && \
    curl -sSL https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list && \
    apt-get update && \
    ACCEPT_EULA=Y apt-get install -y msodbcsql17 && \
    rm -rf /var/lib/apt/lists/*

# Set working directory.
WORKDIR /app

# Copy requirements.txt and install dependencies.
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code.
COPY . .

# Configure nginx
COPY nginx.conf /etc/nginx/sites-available/default
RUN ln -sf /dev/stdout /var/log/nginx/access.log && \
    ln -sf /dev/stderr /var/log/nginx/error.log

# Configure supervisor to run both nginx and gunicorn
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Collect static files if needed
# RUN python manage.py collectstatic --noinput

# Expose port 80 for nginx
EXPOSE 80

# Start services using supervisor
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]