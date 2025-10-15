#!/bin/bash
# Comprehensive static analysis runner for mcp-web
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}   MCP Web Static Analysis${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

cd "$(dirname "$0")/.."

FAILED=0

# Function to run analysis tool
run_analysis() {
    local tool=$1
    local description=$2
    shift 2
    local cmd=("$@")
    
    echo -e "${BLUE}Running $description...${NC}"
    
    if "${cmd[@]}"; then
        echo -e "${GREEN}✓ $description passed${NC}"
        echo ""
        return 0
    else
        echo -e "${RED}✗ $description found issues${NC}"
        echo ""
        return 1
    fi
}

# Ruff linting
run_analysis "ruff" "Ruff Linter" ruff check src/ tests/ || FAILED=1

# Ruff formatting check
run_analysis "ruff" "Ruff Format Check" ruff format --check src/ tests/ || FAILED=1

# MyPy type checking
run_analysis "mypy" "MyPy Type Checking" mypy src/ --ignore-missing-imports || FAILED=1

# Bandit security scanning
echo -e "${BLUE}Running Security Scan (Bandit)...${NC}"
if bandit -r src/ -c .bandit -f screen; then
    echo -e "${GREEN}✓ Security scan passed${NC}"
    echo ""
else
    echo -e "${YELLOW}⚠ Security scan found potential issues${NC}"
    echo ""
    # Don't fail on bandit warnings, just notify
fi

# Semgrep security scanning
if command -v semgrep &> /dev/null; then
    echo -e "${BLUE}Running Semgrep Security Scan...${NC}"
    if semgrep --config=.semgrep.yml src/ --error; then
        echo -e "${GREEN}✓ Semgrep scan passed${NC}"
        echo ""
    else
        echo -e "${YELLOW}⚠ Semgrep found potential issues${NC}"
        echo ""
    fi
else
    echo -e "${YELLOW}Semgrep not installed, skipping${NC}"
    echo ""
fi

# Safety - dependency vulnerability scanning
if command -v safety &> /dev/null; then
    echo -e "${BLUE}Running Dependency Vulnerability Scan (Safety)...${NC}"
    if safety check --json 2>/dev/null; then
        echo -e "${GREEN}✓ No known vulnerabilities in dependencies${NC}"
        echo ""
    else
        echo -e "${YELLOW}⚠ Potential vulnerabilities in dependencies${NC}"
        echo -e "${YELLOW}Run 'safety check' for details${NC}"
        echo ""
    fi
else
    echo -e "${YELLOW}Safety not installed, skipping${NC}"
    echo ""
fi

# Summary
echo -e "${BLUE}======================================${NC}"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All critical checks passed!${NC}"
    exit 0
else
    echo -e "${RED}Some critical checks failed${NC}"
    exit 1
fi
