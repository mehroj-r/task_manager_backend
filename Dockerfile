ARG PYTHON_VERSION=3.13.3
FROM python:${PYTHON_VERSION}-slim AS base

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1
ENV PORT=8080

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/nonexistent" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Upgrade pip to ensure we have the latest version for installing dependencies
RUN pip install --upgrade pip

# Download dependencies.
RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r requirements.txt

# Copy the source code into the container.
COPY . .

# Create a directory for static files
RUN mkdir -p /app/staticfiles

# Collect static files to the specified directory
RUN python manage.py collectstatic --noinput --settings=config.settings.dev

# Ensure proper ownership and permissions
RUN chown -R appuser:appuser /app/staticfiles && \
    chmod -R 755 /app/staticfiles

# Ensure migrations directory exists and has proper permissions
RUN mkdir -p /app/app/migrations && \
    touch /app/app/migrations/__init__.py && \
    chown -R appuser:appuser /app/app/migrations && \
    chmod -R 755 /app/app/migrations

# Create a startup script that will handle migrations and then start the server
RUN echo '#!/bin/bash\n\
echo "Making migrations..."\n\
python manage.py makemigrations --noinput\n\
echo "Applying migrations..."\n\
python manage.py migrate --noinput\n\
echo "Starting server..."\n\
exec gunicorn config.wsgi:application --bind 0.0.0.0:8000\n\
' > /app/start.sh && \
    chmod +x /app/start.sh && \
    chown appuser:appuser /app/start.sh

# Switch to the non-privileged user to run the application.
USER appuser

# Expose the port that the application listens on.
EXPOSE $PORT

# Run the startup script instead of directly running gunicorn
CMD ["/app/start.sh"]