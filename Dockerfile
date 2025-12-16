# Stage 1: Build stage (for collecting staticfiles and installing dependencies)
FROM python:3.11-slim as builder

# Set workdir
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Install pip dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --user -r requirements.txt

# Collect static files (assuming 'manage.py collectstatic' is available)
COPY . .
RUN python manage.py collectstatic --noinput

# Stage 2: Production image
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH="/root/.local/bin:$PATH"

# Copy project files and static assets
COPY . .
COPY --from=builder /app/staticfiles /app/staticfiles

# (Optional) Use a non-root user for security
# RUN groupadd app && useradd -g app app
# USER app

# Expose port (Django default is 8000)
EXPOSE 8000

# Entrypoint (can be adjusted as needed)
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
CMD ["/entrypoint.sh"]