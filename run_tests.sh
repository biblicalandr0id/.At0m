#!/bin/bash
# Convenience script for running consciousness measurement framework tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}======================================${NC}"
echo -e "${GREEN}Consciousness Measurement Framework${NC}"
echo -e "${GREEN}Test Suite Runner${NC}"
echo -e "${GREEN}======================================${NC}"
echo ""

# Check if pytest is installed
if ! command -v pytest &> /dev/null; then
    echo -e "${RED}Error: pytest not found${NC}"
    echo "Install with: pip install pytest pytest-cov pytest-timeout"
    exit 1
fi

# Add consciousness_measurement to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/consciousness_measurement/code"

# Parse command line arguments
TEST_CATEGORY=${1:-all}
VERBOSE=${2:-}

case $TEST_CATEGORY in
    unit)
        echo -e "${YELLOW}Running unit tests...${NC}"
        pytest tests/unit/ -m unit $VERBOSE
        ;;
    integration)
        echo -e "${YELLOW}Running integration tests...${NC}"
        pytest tests/integration/ -m integration $VERBOSE
        ;;
    validation)
        echo -e "${YELLOW}Running validation tests...${NC}"
        pytest tests/validation/ -m validation $VERBOSE
        ;;
    fast)
        echo -e "${YELLOW}Running fast tests (excluding slow tests)...${NC}"
        pytest -m "not slow" $VERBOSE
        ;;
    slow)
        echo -e "${YELLOW}Running slow tests...${NC}"
        pytest -m slow $VERBOSE
        ;;
    coverage)
        echo -e "${YELLOW}Running all tests with coverage...${NC}"
        pytest --cov=consciousness_measurement --cov-report=html --cov-report=term-missing
        echo ""
        echo -e "${GREEN}Coverage report generated: htmlcov/index.html${NC}"
        ;;
    quick)
        echo -e "${YELLOW}Running quick smoke tests...${NC}"
        pytest tests/unit/test_phi_calculator.py::TestPhiCalculatorBasic -v
        ;;
    all)
        echo -e "${YELLOW}Running complete test suite...${NC}"
        pytest tests/ -v --tb=short
        ;;
    *)
        echo -e "${RED}Unknown test category: $TEST_CATEGORY${NC}"
        echo ""
        echo "Usage: $0 [category] [options]"
        echo ""
        echo "Categories:"
        echo "  unit          - Run unit tests only"
        echo "  integration   - Run integration tests only"
        echo "  validation    - Run scientific validation tests"
        echo "  fast          - Run fast tests (exclude slow tests)"
        echo "  slow          - Run slow tests only"
        echo "  coverage      - Run all tests with coverage report"
        echo "  quick         - Quick smoke tests"
        echo "  all           - Run complete test suite (default)"
        echo ""
        echo "Options:"
        echo "  -v            - Verbose output"
        echo "  -vv           - Very verbose output"
        echo "  -x            - Stop on first failure"
        echo "  -s            - Show print statements"
        echo ""
        echo "Examples:"
        echo "  $0                    # Run all tests"
        echo "  $0 unit -v            # Run unit tests verbosely"
        echo "  $0 fast               # Run fast tests only"
        echo "  $0 coverage           # Generate coverage report"
        exit 1
        ;;
esac

EXIT_CODE=$?

echo ""
if [ $EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}======================================${NC}"
    echo -e "${GREEN}✓ All tests passed!${NC}"
    echo -e "${GREEN}======================================${NC}"
else
    echo -e "${RED}======================================${NC}"
    echo -e "${RED}✗ Some tests failed${NC}"
    echo -e "${RED}======================================${NC}"
fi

exit $EXIT_CODE
