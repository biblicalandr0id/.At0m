"""
CONSCIOUSNESS MEASUREMENT FRAMEWORK - TEST SUITE
================================================

Comprehensive validation of consciousness measurement, translation,
preservation, and optimization across all substrates.

Test Structure:
--------------
- unit/: Unit tests for individual components
- integration/: Integration tests across modules
- validation/: Scientific validation tests
- fixtures/: Shared test fixtures and data

Test Categories (pytest markers):
---------------------------------
@pytest.mark.unit - Fast unit tests
@pytest.mark.integration - Cross-module integration
@pytest.mark.validation - Scientific validation
@pytest.mark.slow - Tests > 1 second
@pytest.mark.quantum - Quantum substrate tests
@pytest.mark.gpu - GPU-accelerated tests

Running Tests:
-------------
# All tests
pytest

# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# Validation suite
pytest -m validation

# Fast tests only (exclude slow)
pytest -m "not slow"

# With coverage
pytest --cov

# Verbose output
pytest -vv

Coverage Goals:
--------------
- Line coverage: >90%
- Branch coverage: >85%
- Critical paths: 100%
"""

__version__ = "1.0.0"
__author__ = "Consciousness Measurement Framework Team"
