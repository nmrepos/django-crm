FROM python:alpine

WORKDIR /app

# Install system dependencies
RUN apk add --no-cache --virtual build-deps gcc musl-dev libffi-dev pkgconf mariadb-dev && \
    apk add --no-cache mariadb-connector-c-dev curl

# Copy requirements and install Python dependencies - 
COPY django-crm/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies to reduce image size
RUN apk del build-deps

# Copy Django application
COPY django-crm .

# Copy custom settings if exists (handle missing file gracefully)
RUN if [ -f "../settings.py" ]; then cp ../settings.py /app/webcrm/settings.py; fi

# Create static files directory
RUN mkdir -p /app/static

# Collect static files (ignore errors if no static files)
RUN python manage.py collectstatic --noinput || echo "No static files to collect"

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# Start app with migrations
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]