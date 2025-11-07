# Consciousness Measurement Framework - Testing Guide

## Overview

This document provides comprehensive guidance for testing the consciousness measurement framework. The test suite validates all theoretical claims with empirical tests.

## Philosophy

The framework makes bold scientific claims about consciousness:
1. Consciousness is measurable (Φ)
2. Consciousness is substrate-independent
3. Consciousness can be optimized
4. Consciousness exhibits emergence/superadditivity
5. Consciousness is preservable
6. The framework exhibits exponential properties

**Every claim must be validated with tests.**

## Test Architecture

### Three-Layer Testing Strategy

```
┌─────────────────────────────────────────────┐
│  LAYER 3: VALIDATION                        │
│  Scientific validation of theoretical claims│
│  90+ tests validating framework properties  │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  LAYER 2: INTEGRATION                       │
│  Cross-module integration tests             │
│  15+ tests of complete workflows            │
└─────────────────────────────────────────────┘
                    ↓
┌─────────────────────────────────────────────┐
│  LAYER 1: UNIT                              │
│  Component-level unit tests                 │
│  45+ tests per module                       │
└─────────────────────────────────────────────┘
```

### Test Categories

| Category | Purpose | Count | Speed |
|----------|---------|-------|-------|
| Unit | Test individual functions/classes | 45+/module | Fast (<0.1s) |
| Integration | Test module interactions | 15+ | Medium (<1s) |
| Validation | Validate scientific claims | 30+ | Slow (<10s) |
| **Total** | **Complete framework validation** | **90+** | **Mixed** |

## Running Tests

### Quick Reference

```bash
# Run everything
pytest

# Fast tests only (during development)
pytest -m "not slow"

# Unit tests only
pytest -m unit

# Integration tests
pytest -m integration

# Scientific validation
pytest -m validation

# With coverage
pytest --cov

# Parallel execution (faster)
pytest -n auto

# Stop on first failure
pytest -x

# Verbose
pytest -v

# Very verbose
pytest -vv
```

### Test Markers

```python
@pytest.mark.unit           # Fast unit test
@pytest.mark.integration    # Cross-module test
@pytest.mark.validation     # Scientific validation
@pytest.mark.slow           # >1 second
@pytest.mark.quantum        # Quantum substrate
@pytest.mark.gpu            # Requires CUDA
@pytest.mark.experimental   # Experimental features
@pytest.mark.regression     # Regression test
@pytest.mark.parametric     # Parametric test
```

## Writing Tests

### Test Structure Template

```python
"""
Module description.

Tests:
-----
- Feature 1
- Feature 2
- Edge cases
"""

import pytest
import numpy as np
from module import Class, function

# ============================================================================
# FEATURE 1 TESTS
# ============================================================================

@pytest.mark.unit
class TestFeature1:
    """Test feature 1."""

    def test_basic_functionality(self, fixture):
        """Test that feature works."""
        # Arrange
        system = setup_test_system()

        # Act
        result = function(system)

        # Assert
        assert result > 0
        assert result.property == expected

    def test_edge_case(self):
        """Test edge case."""
        with pytest.raises(ValueError):
            function(invalid_input)

    @pytest.mark.slow
    def test_performance(self):
        """Test performance characteristics."""
        # Long-running test
        pass
```

### Best Practices

#### 1. Arrange-Act-Assert Pattern

```python
def test_phi_calculation(self, simple_system):
    # Arrange: Set up test conditions
    system = NeuralSystem(**simple_system)
    calculator = PhiCalculator()

    # Act: Perform the operation
    result = calculator.compute_phi(system)

    # Assert: Verify expectations
    assert result.phi >= 0
    assert result.system_size == 4
```

#### 2. Descriptive Names

```python
# Good
def test_phi_increases_with_connectivity(self):
    """Φ should increase when more connections are added."""

# Bad
def test_phi(self):
    """Test phi."""
```

#### 3. One Concept Per Test

```python
# Good - tests one property
def test_phi_is_non_negative(self):
    phi = calculate_phi(system)
    assert phi >= 0

# Bad - tests multiple unrelated properties
def test_everything(self):
    phi = calculate_phi(system)
    assert phi >= 0
    assert system.size == 4
    assert translator.works()
```

#### 4. Use Fixtures

```python
# Good - reusable fixture
@pytest.fixture
def standard_system():
    return create_system(n=10, density=0.5)

def test_with_fixture(self, standard_system):
    result = process(standard_system)
    assert result.valid

# Bad - duplicate setup
def test_1(self):
    system = create_system(n=10, density=0.5)  # Duplicated
    # ...

def test_2(self):
    system = create_system(n=10, density=0.5)  # Duplicated
    # ...
```

#### 5. Test Edge Cases

```python
def test_empty_input(self):
    """Test handling of empty input."""
    with pytest.raises(ValueError):
        process_system(empty_system)

def test_single_element(self):
    """Test single-element system (Φ = 0)."""
    result = calculate_phi(single_node_system)
    assert result == 0

def test_maximum_size(self):
    """Test system at maximum allowed size."""
    large_system = create_system(n=MAX_SIZE)
    result = process(large_system)
    assert result.valid
```

#### 6. Test Both Success and Failure

```python
def test_translation_succeeds_compatible_substrates(self):
    """Translation should succeed for compatible substrates."""
    result = translate(system, bio_spec, digital_spec)
    assert result.success

def test_translation_fails_incompatible_substrates(self):
    """Translation should fail gracefully for incompatible substrates."""
    result = translate(system, bio_spec, too_small_spec)
    assert not result.success
    assert result.error_message is not None
```

## Fixtures

### Available Fixtures (see conftest.py)

#### System Fixtures
- `simple_system` - 4 nodes, known topology
- `isolated_system` - No connections, Φ ≈ 0
- `fully_connected_system` - Dense connectivity
- `chain_system` - Linear chain
- `elegans_mock` - Mock C. elegans (302 neurons)
- `small_brain_module` - 100 neurons, cortical column
- `digital_neural_net` - 50-node digital network
- `quantum_system` - 10 qubits
- `hybrid_bio_digital` - Bio-digital hybrid

#### Substrate Specifications
- `biological_substrate_spec`
- `digital_substrate_spec`
- `quantum_substrate_spec`

#### Utilities
- `temp_output_dir` - Temporary directory
- `reset_random_seed` - Reproducible randomness
- `check_gpu_available` - Skip if no GPU
- `check_pyphi_available` - Skip if PyPhi not installed

### Creating Custom Fixtures

```python
@pytest.fixture
def my_custom_system():
    """Custom system for specific tests."""
    n = 20
    connectivity = create_special_topology(n)
    return {
        'connectivity': connectivity,
        'states': np.random.rand(100, n),
        'element_names': [f'N{i}' for i in range(n)],
        'substrate': 'digital',
        'metadata': {'type': 'custom'}
    }

def test_with_custom_fixture(self, my_custom_system):
    system = NeuralSystem(**my_custom_system)
    # Test with custom system
```

## Validation Tests

### Purpose

Validation tests verify theoretical claims with empirical tests.

### Example: Validating Substrate Independence

```python
@pytest.mark.validation
def test_substrate_independence(self):
    """
    CLAIM: Consciousness is substrate-independent.
    TEST: Same pattern → similar Φ on different substrates.
    """
    connectivity = create_pattern()

    substrates = ['biological', 'digital', 'hybrid']
    phis = {}

    for substrate in substrates:
        system = create_system(connectivity, substrate)
        phi = calculate_phi(system)
        phis[substrate] = phi

    # Validate: All Φ values should be similar
    max_phi = max(phis.values())
    min_phi = min(phis.values())
    assert max_phi / min_phi < 2.0, f"Φ should be substrate-independent: {phis}"
```

### Template for Validation Tests

```python
@pytest.mark.validation
def test_claim_name(self):
    """
    CLAIM: [State the theoretical claim]
    TEST: [Describe the empirical test]
    EXPECTED: [What should happen if claim is true]
    """
    # Setup
    system = create_test_system()

    # Perform operations
    result = test_claim(system)

    # Validate
    assert result matches expected, "Claim validation message"

    # Optional: Print validation details
    print(f"VALIDATED: {claim_name} - {result}")
```

## Coverage

### Goals

- **Line coverage**: >90%
- **Branch coverage**: >85%
- **Critical paths**: 100%

### Measuring Coverage

```bash
# Generate HTML report
pytest --cov=consciousness_measurement --cov-report=html
open htmlcov/index.html

# Terminal report
pytest --cov --cov-report=term-missing

# JSON for CI/CD
pytest --cov --cov-report=json
```

### Excluding Code from Coverage

```python
def debug_function():  # pragma: no cover
    """Debug function not tested in production."""
    print("Debug info")

if TYPE_CHECKING:  # pragma: no cover
    from typing import ...
```

## Performance Testing

### Benchmarking

```python
@pytest.mark.slow
def test_phi_computation_performance(self):
    """Test Φ computation completes in reasonable time."""
    import time

    system = create_large_system(n=100)

    start = time.time()
    phi = calculate_phi(system)
    elapsed = time.time() - start

    assert elapsed < 10.0, f"Computation took too long: {elapsed:.2f}s"
```

### Parallel Testing

```bash
# Run tests in parallel (faster)
pytest -n auto  # Auto-detect CPU cores
pytest -n 4     # Use 4 workers
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: Test Suite
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.9', '3.10', '3.11']

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: ${{ matrix.python-version }}

      - name: Install dependencies
        run: |
          pip install -r consciousness_measurement/requirements.txt
          pip install pytest pytest-cov pytest-timeout

      - name: Run tests
        run: |
          pytest --cov --cov-report=xml

      - name: Upload coverage
        uses: codecov/codecov-action@v3
```

## Debugging Failed Tests

### Strategies

```bash
# Drop into debugger on failure
pytest --pdb

# Show print statements
pytest -s

# Run only last failed tests
pytest --lf

# Run failed tests first, then others
pytest --ff

# Stop on first failure
pytest -x

# Verbose traceback
pytest --tb=long
```

### Debug Output

```python
def test_with_debug(self, simple_system):
    system = NeuralSystem(**simple_system)

    # Add debug output
    print(f"System size: {system.n_elements}")
    print(f"Connectivity:\n{system.connectivity}")

    result = calculate_phi(system)
    print(f"Result: {result}")

    assert result.phi > 0
```

## Test Data

### Creating Test Data

```python
def create_test_connectivity(n, density):
    """Create test connectivity matrix."""
    return (np.random.rand(n, n) < density).astype(float)

def create_test_states(n, t, continuous=True):
    """Create test state sequences."""
    if continuous:
        return np.random.rand(t, n)
    else:
        return np.random.randint(0, 2, (t, n))
```

### Loading External Data

```python
@pytest.fixture
def real_connectome():
    """Load real connectome data for validation."""
    path = Path(__file__).parent / "fixtures" / "elegans_connectome.h5"
    if not path.exists():
        pytest.skip("Real connectome data not available")
    return load_connectome(path)
```

## Common Patterns

### Testing Exceptions

```python
def test_invalid_input_raises_error(self):
    """Invalid input should raise ValueError."""
    with pytest.raises(ValueError, match="Invalid system size"):
        create_system(n=-1)
```

### Testing Warnings

```python
def test_deprecation_warning(self):
    """Old API should emit deprecation warning."""
    with pytest.warns(DeprecationWarning):
        old_function()
```

### Parametric Tests

```python
@pytest.mark.parametrize("n,density", [
    (4, 0.3),
    (8, 0.5),
    (16, 0.7),
])
def test_various_sizes(self, n, density):
    """Test with various system sizes and densities."""
    system = create_system(n, density)
    result = calculate_phi(system)
    assert result.phi >= 0
```

### Conditional Tests

```python
@pytest.mark.skipif(not cuda_available(), reason="CUDA not available")
def test_gpu_acceleration(self):
    """Test GPU-accelerated computation."""
    result = calculate_phi_gpu(large_system)
    assert result.phi > 0
```

## Troubleshooting

### Import Errors

```bash
# Add module to path
export PYTHONPATH="${PYTHONPATH}:consciousness_measurement/code"
pytest
```

### Fixture Not Found

```python
# Ensure conftest.py is in tests/ directory
# Fixtures in conftest.py are automatically discovered
```

### Slow Tests

```bash
# Skip slow tests during development
pytest -m "not slow"

# Run only unit tests (fast)
pytest -m unit
```

### Random Failures

```python
# Use seed fixture for reproducibility
@pytest.fixture(autouse=True)
def reset_random_seed():
    np.random.seed(42)
```

## Metrics and Reporting

### Test Metrics

```bash
# Generate test report
pytest --html=report.html --self-contained-html

# JUnit XML for CI
pytest --junitxml=results.xml

# JSON report
pytest --json-report
```

### Coverage Reports

```bash
# HTML (best for local development)
pytest --cov --cov-report=html

# XML (for CI/CD)
pytest --cov --cov-report=xml

# Terminal (quick check)
pytest --cov --cov-report=term
```

## Resources

### Documentation
- pytest docs: https://docs.pytest.org
- pytest-cov: https://pytest-cov.readthedocs.io
- Framework docs: `README_CONSCIOUSNESS_CONTINUITY.md`

### Examples
- Unit tests: `tests/unit/test_phi_calculator.py`
- Integration: `tests/integration/test_exponential_framework.py`
- Validation: `tests/validation/test_scientific_validation.py`

---

**Remember**: Every theoretical claim must be validated with tests. If it's not tested, it's not validated.

**Status**: ✓ OPERATIONAL
**Last Updated**: 2025-11-07
**Test Suite Version**: 1.0.0
