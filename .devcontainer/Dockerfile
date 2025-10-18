# Development container for mcp-web project
# Based on Debian 12 with uv, Python, and development tools

ARG BASE="debian-12"
FROM mcr.microsoft.com/devcontainers/base:${BASE}

# Install system dependencies
# - build-essential: C/C++ compilers for native extensions
# - libssl-dev: SSL/TLS support
# - libffi-dev: Foreign Function Interface support
# - curl: Download tools
# - git: Version control (usually pre-installed)
RUN apt-get clean && \
    apt-get update && \
    apt-get install -y \
        build-essential \
        libssl-dev \
        libffi-dev \
        curl \
        git \
        # Playwright dependencies
        libnss3 \
        libnspr4 \
        libatk1.0-0 \
        libatk-bridge2.0-0 \
        libcups2 \
        libdrm2 \
        libdbus-1-3 \
        libxkbcommon0 \
        libxcomposite1 \
        libxdamage1 \
        libxfixes3 \
        libxrandr2 \
        libgbm1 \
        libpango-1.0-0 \
        libcairo2 \
        libasound2 \
        libatspi2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV HOME="/home/vscode"
ENV UV_CACHE_DIR="/home/vscode/.cache/uv"
ENV PYTHONPATH="/workspaces/mcp-web/src"

# Switch to non-root user
USER vscode
WORKDIR /home/vscode

# Install uv (Python package manager)
# Using official uv Docker image for optimal setup
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv
COPY --from=ghcr.io/astral-sh/uv:latest /uvx /usr/local/bin/uvx

# Install Python 3.10 (minimum required version)
ARG PYTHON_VERSION=3.10
RUN uv python install ${PYTHON_VERSION}

# Install Task runner (task command for Taskfile)
USER root
RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d
USER vscode

# Create cache directories
RUN mkdir -p /home/vscode/.cache/uv \
    && mkdir -p /home/vscode/.cache/mcp-web \
    && mkdir -p /home/vscode/.cache/pytest

# Set working directory to project root
WORKDIR /workspaces/mcp-web

# The actual project setup (dependencies, Playwright browsers) happens in postCreateCommand
# to take advantage of Docker layer caching and to work with the mounted workspace
