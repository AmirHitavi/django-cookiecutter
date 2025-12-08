# Use official Python 3.11.12 on Debian Bullseye as the base image
FROM python:3.11.12-bullseye AS python-base

# Prevent Python from writing .pyc files and enable unbuffered stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app


# Builder stage for compiling dependencies and wheels
FROM python-base AS builder

# Define build-time argument for environment (local, production, etc.)
ARG BUILD_ENVIRONMENT=local

# Update package lists and install build tools and libraries required for compiling Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libmagic-dev \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Copy the requirements folder into the container
COPY ./requirements /app/requirements

# Build wheels for Python dependencies to optimize installation later
RUN pip wheel --no-cache-dir -r /app/requirements/${BUILD_ENVIRONMENT}.txt -w /wheels


# Runtime stage for running the application
FROM python-base AS runtime

# Define build-time arguments
ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

# Install only runtime dependencies needed by Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*  # Clean up apt cache to reduce image size

# Create a non-root user for running Django
RUN adduser --disabled-password --no-create-home django_user

# Create directories for static files and media and set ownership to non-root user
RUN mkdir -p /vol/web/static /vol/web/media \
    && chown -R django_user:django_user /vol

# Copy pre-built wheels from the builder stage
COPY --from=builder /wheels /wheels

# Switch to non-root user
USER django_user

# Install Python dependencies from wheels and remove wheel files to save space
RUN pip install --no-cache-dir /wheels/*.whl \
    && rm -rf /wheels

# Copy and prepare entrypoint script (convert Windows line endings and make executable)
COPY ./docker/local/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

# Copy and prepare start script
COPY ./docker/local/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh && chmod +x /start.sh

# Conditional: if Celery is used, copy worker and Flower start scripts
{% if cookiecutter.use_celery == 'y' %}
COPY ./docker/local/django/celery/worker/start.sh /worker.sh
RUN sed -i 's/\r$//g' /worker.sh && chmod +x /worker.sh

COPY ./docker/local/django/celery/flower/start.sh /flower.sh
RUN sed -i 's/\r$//g' /flower.sh && chmod +x /flower.sh
{% endif %}

# Conditional: if Celery Beat is used, copy Beat start script
{% if cookiecutter.use_celery == 'y' and cookiecutter.use_beat == 'y' %}
COPY ./docker/local/django/celery/beat/start.sh /beat.sh
RUN sed -i 's/\r$//g' /beat.sh && chmod +x /beat.sh
{% endif %}

# Copy the full Django application code into the container
COPY . ${APP_HOME}

# Ensure the non-root user owns the application code
RUN chown -R django_user:django_user ${APP_HOME}

# Set the container entrypoint to the entrypoint script
ENTRYPOINT ["/entrypoint.sh"]