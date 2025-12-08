FROM python:3.11.12-bullseye AS python-base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app


FROM python-base AS builder

ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libmagic-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements folder
COPY ./requirements /app/requirements

# Create wheels output dir
RUN mkdir -p /wheels

# BUILD_ENVIRONMENT.txt must exist under /requirements/*.txt
RUN pip wheel --no-cache-dir \
    -r requirements/${BUILD_ENVIRONMENT}.txt \
    --wheel-dir /wheels


FROM python-base AS runtime

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    libmagic1 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN adduser --disabled-password --no-create-home django_user

# Create static/media volumes
RUN mkdir -p /vol/web/static /vol/web/media \
    && chown -R django_user:django_user /vol

# Copy wheels from builder
COPY --from=builder /wheels /wheels

# Install wheels
RUN pip install --no-cache-dir /wheels/*.whl \
    && rm -rf /wheels

USER django_user

# Entrypoint and start script
COPY ./docker/local/django/entrypoint.sh /entrypoint.sh
RUN sed -i 's/\r$//g' /entrypoint.sh && chmod +x /entrypoint.sh

COPY ./docker/local/django/start.sh /start.sh
RUN sed -i 's/\r$//g' /start.sh && chmod +x /start.sh

# Celery (if enabled)
{% if cookiecutter.use_celery == 'y' %}
COPY ./docker/local/django/celery/worker/start.sh /worker.sh
RUN sed -i 's/\r$//g' /worker.sh && chmod +x /worker.sh

COPY ./docker/local/django/celery/flower/start.sh /flower.sh
RUN sed -i 's/\r$//g' /flower.sh && chmod +x /flower.sh
{% endif %}

{% if cookiecutter.use_celery == 'y' and cookiecutter.use_beat == 'y' %}
COPY ./docker/local/django/celery/beat/start.sh /beat.sh
RUN sed -i 's/\r$//g' /beat.sh && chmod +x /beat.sh
{% endif %}

# Copy full application code
COPY . ${APP_HOME}

RUN chown -R django_user:django_user ${APP_HOME}

ENTRYPOINT ["/entrypoint.sh"]