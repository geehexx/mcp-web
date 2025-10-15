#!/bin/bash
# Comprehensive test runner for mcp-web
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}======================================${NC}"
echo -e "${BLUE}   MCP Web Test Suite Runner${NC}"
echo -e "${BLUE}======================================${NC}"
echo ""

# Change to project root
cd "$(dirname "$0")/.."

# Check for virtual environment
if [ -z "$VIRTUAL_ENV" ]; then
    echo -e "${YELLOW}Warning: No virtual environment detected${NC}"
    echo -e "${YELLOW}Consider activating a virtual environment first${NC}"
    echo ""
fi

# Parse arguments
RUN_UNIT=true
RUN_INTEGRATION=false
RUN_SECURITY=true
RUN_GOLDEN=true
RUN_LIVE=false
RUN_BENCHMARKS=false
RUN_COVERAGE=true
PARALLEL=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --all)
            RUN_UNIT=true
            RUN_INTEGRATION=true
            RUN_SECURITY=true
            RUN_GOLDEN=true
            shift
            ;;
        --live)
            RUN_LIVE=true
            shift
            ;;
        --bench)
            RUN_BENCHMARKS=true
            shift
            ;;
        --integration)
            RUN_INTEGRATION=true
            shift
            ;;
        --no-coverage)
            RUN_COVERAGE=false
            shift
            ;;
        --parallel)
            PARALLEL=true
            shift
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Build pytest command
PYTEST_ARGS=""

if [ "$RUN_COVERAGE" = true ]; then
    PYTEST_ARGS="$PYTEST_ARGS --cov=mcp_web --cov-report=term-missing --cov-report=html"
fi

if [ "$PARALLEL" = true ]; then
    PYTEST_ARGS="$PYTEST_ARGS -n auto"
fi

# Function to run test category
run_test_category() {
    local category=$1
    local marker=$2
    local description=$3
    
    echo -e "${BLUE}Running $description...${NC}"
    
    if pytest -m "$marker" $PYTEST_ARGS; then
        echo -e "${GREEN}✓ $description passed${NC}"
        echo ""
        return 0
    else
        echo -e "${RED}✗ $description failed${NC}"
        echo ""
        return 1
    fi
}

# Run test categories
FAILED=0

if [ "$RUN_UNIT" = true ]; then
    run_test_category "unit" "unit" "Unit Tests" || FAILED=1
fi

if [ "$RUN_SECURITY" = true ]; then
    run_test_category "security" "security" "Security Tests" || FAILED=1
fi

if [ "$RUN_GOLDEN" = true ]; then
    run_test_category "golden" "golden" "Golden/Regression Tests" || FAILED=1
fi

if [ "$RUN_INTEGRATION" = true ]; then
    run_test_category "integration" "integration" "Integration Tests" || FAILED=1
fi

if [ "$RUN_LIVE" = true ]; then
    if [ -z "$OPENAI_API_KEY" ]; then
        echo -e "${YELLOW}Skipping live tests: OPENAI_API_KEY not set${NC}"
        echo ""
    else
        run_test_category "live" "live" "Live Tests" || FAILED=1
    fi
fi

if [ "$RUN_BENCHMARKS" = true ]; then
    run_test_category "benchmarks" "benchmark" "Performance Benchmarks" || FAILED=1
fi

# Summary
echo -e "${BLUE}======================================${NC}"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed${NC}"
    exit 1
fi
