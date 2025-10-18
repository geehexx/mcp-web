# Development Container Configuration

This directory contains the configuration for VS Code Development Containers, providing a consistent, reproducible development environment for mcp-web.

## Files

### `Dockerfile`

Defines the container image based on Debian 12 with:
- Python 3.10 (via uv package manager)
- System dependencies for Playwright
- Task runner for automation
- Non-root `vscode` user for security

**Key decisions:**
- Base: `mcr.microsoft.com/devcontainers/base:debian-12` for flexibility
- uv: Modern Python package manager (faster than pip)
- Playwright deps: Pre-installed to avoid runtime issues

### `devcontainer.json`

VS Code configuration including:
- Build arguments (Python version, base image)
- Editor settings (Python, Ruff, Mypy)
- Extensions (Python, Ruff, Mypy, Task, Git, Docker, etc.)
- Features (Docker-in-Docker, GitHub CLI)
- Post-create command hook

**Key decisions:**
- Python interpreter path: `/home/vscode/.local/share/uv/python`
- Format on save with Ruff
- pytest integration for testing
- Task runner for automation commands

### `post-create.sh`

Automated setup script that runs after container creation:
1. Install project dependencies (`uv sync --all-extras`)
2. Install Playwright browsers (`playwright install chromium`)
3. Configure pre-commit hooks
4. Create cache directories
5. Display environment info

**Runs automatically** - no manual intervention needed.

## Usage

### First Time Setup

1. Install prerequisites:
   - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
   - [VS Code](https://code.visualstudio.com/)
   - [Dev Containers Extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

2. Open project in VS Code:
   ```bash
   code .
   ```

3. Reopen in container:
   - Click "Reopen in Container" when prompted
   - Or: Press F1 → "Dev Containers: Reopen in Container"

4. Wait for setup (~2-5 minutes first time)

### Daily Development

Once set up, the container starts quickly (10-30 seconds). All your tools and dependencies are ready.

```bash
# Run tests
task test:fast

# Run linting
task lint

# See all commands
task --list
```

### Customization

#### Change Python Version

Edit `devcontainer.json`:

```json
"args": {
  "PYTHON_VERSION": "3.11"
}
```

Then rebuild: F1 → "Dev Containers: Rebuild Container"

#### Add VS Code Extensions

Edit `devcontainer.json`:

```json
"extensions": [
  "ms-python.python",
  "your-extension-id"
]
```

**Note:** Some IDEs (like Windsurf) may have restrictions on third-party extensions. For standard VS Code, all listed extensions are valid and recommended.

#### Add System Dependencies

Edit `Dockerfile`:

```dockerfile
RUN apt-get update && apt-get install -y \
    your-package-here \
    another-package
```

#### Modify Post-Create Script

Edit `post-create.sh` to add custom setup steps:

```bash
#!/bin/bash
# ... existing setup ...

# Your custom setup
echo "Running custom setup..."
# commands here
```

## Troubleshooting

### Container Build Fails

**Symptom:** Error during "Building container" step

**Solutions:**
1. Check Docker is running: `docker ps`
2. Clear Docker cache:
   ```bash
   docker system prune -a
   ```
3. Rebuild without cache:
   - F1 → "Dev Containers: Rebuild Container"
   - Select "Rebuild Without Cache"

### Extensions Not Working

**Symptom:** Python, Ruff, or other extensions not functioning

**Solutions:**
1. Reload window: F1 → "Developer: Reload Window"
2. Reinstall extensions: F1 → "Dev Containers: Rebuild Container"
3. Check extension compatibility with your IDE

### Slow Performance

**Symptom:** Container operations are slow

**Solutions:**
1. Allocate more resources in Docker Desktop:
   - Settings → Resources → Increase CPU/Memory
2. On Windows: Use WSL 2 backend
   - Docker Desktop → Settings → General → Use WSL 2 engine
3. Enable BuildKit for faster builds:
   ```bash
   export DOCKER_BUILDKIT=1
   ```

### Playwright Browsers Missing

**Symptom:** Integration tests fail with browser not found

**Solutions:**
1. Reinstall browsers:
   ```bash
   uv run playwright install chromium
   ```
2. Check post-create.sh ran successfully:
   ```bash
   cat ~/.devcontainer-setup.log
   ```

### Permission Issues

**Symptom:** Can't write files or access directories

**Solutions:**
1. Ensure `remoteUser` is set to `vscode` in `devcontainer.json`
2. Check file ownership in container:
   ```bash
   ls -la
   ```
3. Fix ownership if needed:
   ```bash
   sudo chown -R vscode:vscode /workspaces/mcp-web
   ```

## Architecture

### Container Layers

```text
1. Base: mcr.microsoft.com/devcontainers/base:debian-12
   ↓
2. System packages (build-essential, Playwright deps)
   ↓
3. User setup (vscode user, home directory)
   ↓
4. uv installation (Python package manager)
   ↓
5. Python 3.10 installation
   ↓
6. Task runner installation
   ↓
7. Cache directories
```

### Post-Create Flow

```text
Container starts
   ↓
Mount workspace
   ↓
Run post-create.sh
   ├── uv sync (install deps)
   ├── playwright install
   ├── pre-commit install
   └── setup cache dirs
   ↓
Ready for development
```

## Best Practices

### DO ✅

- Use the container for all development
- Commit from inside the container
- Run tests inside the container
- Keep container updated (rebuild periodically)
- Document custom setup in post-create.sh

### DON'T ❌

- Mix local and container Python environments
- Install system packages without updating Dockerfile
- Commit container-specific paths to git
- Manually install tools (use post-create.sh)
- Ignore rebuild prompts after config changes

## Performance Optimization

### Docker Layer Caching

The Dockerfile is structured to maximize layer caching:
1. System packages (changes rarely)
2. uv installation (changes rarely)
3. Python installation (changes with version bumps)
4. Dependencies (changes with pyproject.toml updates)

### Volume Mounts

The container uses Docker volumes for:
- `/home/vscode/.cache` - Persistent caching across rebuilds
- `/workspaces/mcp-web` - Your project files

### uv Cache

uv caching is enabled via `UV_CACHE_DIR`, significantly speeding up:
- `uv sync` operations
- Python package downloads
- Dependency resolution

## References

- [VS Code Dev Containers Documentation](https://code.visualstudio.com/docs/devcontainers/containers)
- [Dev Container Specification](https://containers.dev/)
- [Dev Container Features](https://containers.dev/features)
- [uv Documentation](https://docs.astral.sh/uv/)
- [Playwright Installation](https://playwright.dev/python/docs/intro)

## Support

If you encounter issues not covered here:
1. Check [main README.md](../README.md#development-containers)
2. Check [CONTRIBUTING.md](../CONTRIBUTING.md#getting-started)
3. Open an issue on GitHub

---

**Maintained by:** mcp-web contributors
**Last updated:** 2025-10-19
