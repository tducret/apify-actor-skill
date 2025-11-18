# syntax=docker/dockerfile:1.6

# Build stage - install dependencies and build artifacts
FROM apify/actor-python:3.13 AS builder

# Set working directory
WORKDIR /app

# Install uv as root
USER root
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/* \
    && curl -LsSf https://astral.sh/uv/install.sh | sh \
    && mv /root/.local/bin/uv /usr/local/bin/uv

# Copy dependency files first for better layer caching
COPY pyproject.toml uv.lock* ./

# Copy source code (needed for editable install)
COPY src/ ./src/

# Install dependencies (creates .venv by default)
RUN uv sync --frozen --no-dev

# Pre-compile Python files with optimization for faster startup
RUN python3 -O -m compileall -q src/

# Runtime stage - minimal image with only runtime dependencies
FROM apify/actor-python:3.13 AS runtime

# Set working directory
WORKDIR /app

# Copy the virtual environment from builder stage
COPY --from=builder /app/.venv /app/.venv

# Copy source code and compiled Python files
COPY --from=builder /app/src /app/src

# Copy any other necessary application files
COPY --chown=myuser:myuser . .

# Switch to non-root user for security
USER myuser

# Ensure the venv is in PATH for the myuser context
ENV PATH="/app/.venv/bin:$PATH"

# Run the actor module
CMD ["python3", "-m", "src.main"]
