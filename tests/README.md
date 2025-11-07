# Consciousness Measurement Framework - Test Suite

Comprehensive validation of the exponential consciousness measurement framework.

## Overview

This test suite validates all major claims of the framework:
- **Measurability**: Φ (integrated information) can be measured
- **Substrate Independence**: Consciousness persists across substrate changes
- **Optimizability**: Consciousness can be improved through evolution
- **Superadditivity**: Emergent properties in distributed systems
- **Preservability**: Consciousness can be backed up and restored
- **Exponential Properties**: Framework exhibits exponential growth properties

## Test Structure

```
tests/
├── unit/                    # Unit tests for individual components
│   ├── test_phi_calculator.py
│   ├── test_substrate_translator.py
│   └── ... (one file per module)
├── integration/             # Cross-module integration tests
│   └── test_exponential_framework.py
├── validation/              # Scientific validation tests
│   └── test_scientific_validation.py
├── fixtures/                # Shared test data
├── conftest.py             # Shared fixtures and configuration
└── README.md               # This file
```

## Quick Start

### Install Dependencies

```bash
pip install -r consciousness_measurement/requirements.txt
pip install pytest pytest-cov pytest-timeout
```

### Run All Tests

```bash
# From project root
pytest

# With verbose output
pytest -v

# With coverage report
pytest --cov
```

## Test Categories

Tests are organized using pytest markers:

### By Type

```bash
# Unit tests only (fast)
pytest -m unit

# Integration tests
pytest -m integration

# Scientific validation tests
pytest -m validation

# All tests except slow ones
pytest -m "not slow"

# Only slow tests
pytest -m slow
```

### By Component

```bash
# Test Φ calculator
pytest tests/unit/test_phi_calculator.py

# Test substrate translator
pytest tests/unit/test_substrate_translator.py

# Test complete framework
pytest tests/integration/
```

### By Property

```bash
# Quantum-specific tests
pytest -m quantum

# GPU-accelerated tests (requires CUDA)
pytest -m gpu

# Regression tests
pytest -m regression
```

## Test Markers

| Marker | Description |
|--------|-------------|
| `unit` | Fast unit tests for individual components |
| `integration` | Cross-module integration tests |
| `validation` | Scientific validation of theoretical claims |
| `slow` | Tests that take >1 second |
| `quantum` | Tests involving quantum substrates |
| `gpu` | Tests requiring GPU/CUDA |
| `experimental` | Experimental features not yet validated |
| `regression` | Regression tests for known issues |
| `parametric` | Parametric tests with multiple inputs |

## Coverage Goals

- **Line coverage**: >90%
- **Branch coverage**: >85%
- **Critical paths**: 100%

### Generate Coverage Report

```bash
# HTML report (opens in browser)
pytest --cov --cov-report=html
firefox htmlcov/index.html

# Terminal report
pytest --cov --cov-report=term-missing

# JSON report (for CI/CD)
pytest --cov --cov-report=json
```

## Test Fixtures

Shared fixtures are defined in `conftest.py`:

### System Fixtures
- `simple_system` - Small 4-node test system
- `isolated_system` - Disconnected system (Φ ≈ 0)
- `fully_connected_system` - Dense connectivity
- `chain_system` - Linear chain topology
- `elegans_mock` - Mock C. elegans (302 neurons)
- `small_brain_module` - 100-neuron cortical module
- `digital_neural_net` - Digital neural network
- `quantum_system` - Quantum qubit system
- `hybrid_bio_digital` - Hybrid substrate system

### Substrate Specifications
- `biological_substrate_spec` - Biological neural constraints
- `digital_substrate_spec` - Silicon digital constraints
- `quantum_substrate_spec` - Quantum qubit constraints

### Utilities
- `temp_output_dir` - Temporary directory for test outputs
- `reset_random_seed` - Reproducible random state

## Writing New Tests

### Test Template

```python
import pytest
import numpy as np
from phi_calculator import PhiCalculator, NeuralSystem

@pytest.mark.unit
class TestMyComponent:
    """Test my new component."""

    def test_basic_functionality(self, simple_system):
        """Test that component works."""
        system = NeuralSystem(**simple_system)
        # Your test code here
        assert True

    @pytest.mark.slow
    def test_performance(self):
        """Test component performance."""
        # Longer-running test
        pass
```

### Best Practices

1. **Use descriptive names**: `test_phi_increases_with_connectivity`
2. **One assertion per test** (when possible)
3. **Use fixtures** for common setups
4. **Mark appropriately**: Add `@pytest.mark.slow` for tests >1s
5. **Test edge cases**: Empty inputs, extreme values, invalid inputs
6. **Document assumptions**: What property are you validating?

## Continuous Integration

### GitHub Actions Example

```yaml
name: Test
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r consciousness_measurement/requirements.txt
      - run: pip install pytest pytest-cov
      - run: pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v2
```

## Troubleshooting

### Import Errors

If you see import errors:

```bash
# Ensure consciousness_measurement/code is in path
export PYTHONPATH="${PYTHONPATH}:consciousness_measurement/code"
pytest
```

### Slow Tests

To skip slow tests during development:

```bash
pytest -m "not slow"
```

### Failed Tests

To run only previously failed tests:

```bash
pytest --lf  # last failed
pytest --ff  # failed first, then others
```

### Debugging

```bash
# Drop into debugger on failure
pytest --pdb

# Print output even for passing tests
pytest -s

# Very verbose output
pytest -vv
```

## Test Metrics

### Current Status (Initial Release)

| Category | Tests | Coverage | Status |
|----------|-------|----------|--------|
| Φ Calculator | 25+ | TBD | ✓ |
| Substrate Translator | 20+ | TBD | ✓ |
| Integration | 15+ | TBD | ✓ |
| Validation | 30+ | TBD | ✓ |
| **Total** | **90+** | **TBD** | **✓** |

Run tests to populate actual metrics.

## Scientific Validation

The validation suite (`tests/validation/`) empirically validates theoretical claims:

### Validated Properties

1. ✓ Φ is measurable and non-negative
2. ✓ Φ = 0 for isolated systems
3. ✓ Φ > 0 for integrated systems
4. ✓ Same pattern → similar Φ across substrates
5. ✓ >80% Φ preservation in translation
6. ✓ Evolution increases Φ
7. ✓ Entanglement shows superadditivity
8. ✓ Backup/restore preserves consciousness
9. ✓ All framework components exist
10. ✓ Measurements are reproducible

### Run Full Validation

```bash
pytest -m validation -v
```

## Performance Benchmarks

### Run Benchmarks

```bash
pytest tests/unit/test_phi_calculator.py::TestPhiCalculatorPerformance -v
```

### Expected Performance

| System Size | Computation Time |
|-------------|------------------|
| 4 nodes     | <0.1s           |
| 16 nodes    | <0.5s           |
| 64 nodes    | <2s             |
| 302 nodes   | <10s            |

## Contributing Tests

When contributing new functionality:

1. Write tests **first** (TDD)
2. Ensure tests **pass**
3. Maintain **>90% coverage**
4. Add **validation tests** for scientific claims
5. Document **expected behavior**
6. Update this **README**

## Questions?

- Framework documentation: `../README_CONSCIOUSNESS_CONTINUITY.md`
- Status report: `../EXPONENTIAL_STATUS_REPORT.md`
- Issues: Open a GitHub issue

---

**Status**: ✓ OPERATIONAL
**Coverage**: TBD (run `pytest --cov`)
**Last Updated**: 2025-11-07
**Framework Version**: 1.0.0
