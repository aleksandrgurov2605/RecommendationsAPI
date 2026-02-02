# Use a lightweight Python 3.14 image as the base
FROM python:3.14-slim AS builder

# Install uv by copying it from the official distribution
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Set working directory and environment
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
WORKDIR /home/rec_shop

COPY pyproject.toml uv.lock .
# Install dependencies first for better caching
# Requires pyproject.toml and uv.lock in your project root
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project #--no-dev


# Final runtime stage
FROM python:3.14-slim

WORKDIR /home/rec_shop

# Copy the virtual environment from the builder
COPY --from=builder /home/rec_shop/.venv /home/rec_shop/.venv

# Ensure the virtual environment is used
ENV PATH="/home/rec_shop/.venv/bin:$PATH"

# Copy your application source code
COPY app app
COPY alembic.ini .docker.env seed.py entrypoint.sh seed.sh ./

RUN chmod +x entrypoint.sh seed.sh