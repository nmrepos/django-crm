# Container image for the Django CRM application.
# Build it from the repository root, with the CRM source cloned into ./django-crm.

# Small Python base image built on Alpine Linux
FROM python:alpine

# All application files live in /app inside the container
WORKDIR /app

# Install system dependencies.
# build-deps holds the compilers and headers needed to build the MySQL driver
# (mysqlclient). It is removed again further down to keep the image small.
# mariadb-connector-c-dev is the runtime MySQL client library, and curl is
# used by the health check.
RUN apk add --no-cache --virtual build-deps gcc musl-dev libffi-dev pkgconf mariadb-dev && \
    apk add --no-cache mariadb-connector-c-dev curl

# Copy requirements and install Python dependencies.
# This is done before copying the rest of the code so Docker can cache this
# layer and skip reinstalling packages when only the code changes.
COPY django-crm/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Remove build dependencies to reduce image size
RUN apk del build-deps

# Copy the Django application source into /app
COPY django-crm .

# Copy custom settings if the file exists (handle a missing file gracefully).
# Note: ../settings.py is outside the build context, so this step normally does
# nothing. Copy settings.py into django-crm/webcrm/ before building instead.
RUN if [ -f "../settings.py" ]; then cp ../settings.py /app/webcrm/settings.py; fi

# Create the directory that collectstatic writes to (STATIC_ROOT)
RUN mkdir -p /app/static

# Collect static files (CSS, JavaScript, images) into /app/static.
# Errors are ignored so the build still succeeds if there is nothing to collect.
RUN python manage.py collectstatic --noinput || echo "No static files to collect"

# The Django development server listens on this port
EXPOSE 8080

# Health check: Docker marks the container unhealthy if the home page
# stops responding
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8080/ || exit 1

# On every start, apply any pending database migrations and then run the
# Django server on all interfaces, port 8080
CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8080"]
