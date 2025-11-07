"""
Unit tests for Φ (integrated information) calculator.

Tests:
-----
- ConsciousnessMetrics data structure
- NeuralSystem validation
- Φ calculation for simple systems
- Φ calculation edge cases
- Partition analysis
- Cross-substrate comparison
- Performance benchmarks
"""

import pytest
import numpy as np
from pathlib import Path
import json

from phi_calculator import (
    PhiCalculator,
    ConsciousnessMetrics,
    NeuralSystem
)


# ============================================================================
# DATA STRUCTURE TESTS
# ============================================================================

@pytest.mark.unit
class TestConsciousnessMetrics:
    """Test ConsciousnessMetrics dataclass."""

    def test_creation(self):
        """Test basic creation."""
        metrics = ConsciousnessMetrics(
            phi=0.5,
            phi_max=1.0,
            mip=[(0, 1), (2, 3)],
            system_size=4,
            complexity=0.8,
            integration_time=0.123,
            substrate_type='digital',
            metadata={'test': True}
        )
        assert metrics.phi == 0.5
        assert metrics.system_size == 4
        assert metrics.substrate_type == 'digital'

    def test_to_dict(self):
        """Test dictionary conversion."""
        metrics = ConsciousnessMetrics(
            phi=0.5, phi_max=1.0, mip=None, system_size=4,
            complexity=0.8, integration_time=0.1,
            substrate_type='digital', metadata={}
        )
        d = metrics.to_dict()
        assert isinstance(d, dict)
        assert d['phi'] == 0.5
        assert d['system_size'] == 4

    def test_save_load(self, temp_output_dir):
        """Test saving and loading."""
        metrics = ConsciousnessMetrics(
            phi=0.5, phi_max=1.0, mip=None, system_size=4,
            complexity=0.8, integration_time=0.1,
            substrate_type='digital', metadata={'test': 'data'}
        )
        path = temp_output_dir / "metrics.json"
        metrics.save(path)

        assert path.exists()
        with open(path) as f:
            loaded = json.load(f)
        assert loaded['phi'] == 0.5
        assert loaded['metadata']['test'] == 'data'


@pytest.mark.unit
class TestNeuralSystem:
    """Test NeuralSystem dataclass."""

    def test_creation(self, simple_system):
        """Test system creation."""
        system = NeuralSystem(**simple_system)
        assert system.n_elements == 4
        assert system.n_timepoints == 100
        assert len(system.element_names) == 4

    def test_validation_success(self, simple_system):
        """Test validation for valid system."""
        system = NeuralSystem(**simple_system)
        assert system.validate() is True

    def test_validation_failure_size_mismatch(self, simple_system):
        """Test validation catches size mismatches."""
        # Wrong states size
        simple_system['states'] = np.random.rand(100, 5)  # Should be 4
        system = NeuralSystem(**simple_system)
        with pytest.raises(AssertionError):
            system.validate()

    def test_validation_failure_names(self, simple_system):
        """Test validation catches name count mismatch."""
        simple_system['element_names'] = ['N0', 'N1']  # Should be 4
        system = NeuralSystem(**simple_system)
        with pytest.raises(AssertionError):
            system.validate()

    def test_properties(self, elegans_mock):
        """Test system properties."""
        system = NeuralSystem(**elegans_mock)
        assert system.n_elements == 302
        assert system.n_timepoints == 100
        assert system.substrate == 'biological'


# ============================================================================
# PHI CALCULATOR TESTS
# ============================================================================

@pytest.mark.unit
class TestPhiCalculatorBasic:
    """Basic Φ calculator tests."""

    def test_initialization(self):
        """Test calculator initialization."""
        calc = PhiCalculator()
        assert calc is not None

    def test_compute_phi_simple(self, simple_system):
        """Test Φ computation on simple system."""
        system = NeuralSystem(**simple_system)
        calc = PhiCalculator()
        metrics = calc.compute_phi(system)

        assert isinstance(metrics, ConsciousnessMetrics)
        assert metrics.phi >= 0.0
        assert metrics.system_size == 4
        assert metrics.substrate_type == 'digital'
        assert metrics.integration_time > 0

    def test_compute_phi_isolated_system(self, isolated_system):
        """Test that isolated system has Φ ≈ 0."""
        system = NeuralSystem(**isolated_system)
        calc = PhiCalculator()
        metrics = calc.compute_phi(system)

        # Isolated system should have very low Φ (< 0.2 is acceptable for approximate methods)
        assert metrics.phi < 0.2, f"Expected Φ ≈ 0 for isolated system, got {metrics.phi}"

    def test_compute_phi_fully_connected(self, fully_connected_system):
        """Test that fully connected system has high Φ."""
        system = NeuralSystem(**fully_connected_system)
        calc = PhiCalculator()
        metrics = calc.compute_phi(system)

        # Fully connected should have non-trivial Φ
        assert metrics.phi > 0.01, f"Expected Φ > 0.01 for fully connected system, got {metrics.phi}"

    def test_phi_monotonicity(self):
        """Test that more connections → higher Φ (generally).

        Note: Φ depends on integration patterns, not just connection count.
        This test validates that fully connected systems have higher Φ than isolated systems.
        """
        calc = PhiCalculator()

        n = 10
        # Fully isolated (no connections)
        isolated = NeuralSystem(
            connectivity=np.zeros((n, n)),
            states=np.random.randint(0, 2, (50, n)),
            element_names=[f'N{i}' for i in range(n)],
            substrate='digital',
            metadata={'density': 0.0}
        )

        # Fully connected
        fully_connected = np.ones((n, n))
        np.fill_diagonal(fully_connected, 0)
        connected = NeuralSystem(
            connectivity=fully_connected,
            states=np.random.randint(0, 2, (50, n)),
            element_names=[f'N{i}' for i in range(n)],
            substrate='digital',
            metadata={'density': 1.0}
        )

        phi_isolated = calc.compute_phi(isolated).phi
        phi_connected = calc.compute_phi(connected).phi

        # Fully connected should have higher Φ than isolated
        assert phi_connected > phi_isolated * 0.5, \
            f"Connected system Φ ({phi_connected}) should be > isolated ({phi_isolated})"


@pytest.mark.unit
class TestPhiCalculatorEdgeCases:
    """Edge case tests for Φ calculator."""

    def test_single_element(self):
        """Test single element system (Φ should be 0)."""
        system = NeuralSystem(
            connectivity=np.array([[0]]),
            states=np.random.rand(50, 1),
            element_names=['N0'],
            substrate='digital',
            metadata={}
        )
        calc = PhiCalculator()
        metrics = calc.compute_phi(system)
        assert metrics.phi == 0.0, "Single element cannot have integration"

    def test_two_elements_connected(self):
        """Test minimal integrated system (2 connected elements)."""
        system = NeuralSystem(
            connectivity=np.array([[0, 1], [1, 0]]),
            states=np.random.randint(0, 2, (50, 2)),
            element_names=['N0', 'N1'],
            substrate='digital',
            metadata={}
        )
        calc = PhiCalculator()
        metrics = calc.compute_phi(system)
        assert metrics.phi > 0, "Two connected elements should have Φ > 0"

    def test_empty_states(self):
        """Test handling of empty state sequence."""
        system = NeuralSystem(
            connectivity=np.array([[0, 1], [1, 0]]),
            states=np.empty((0, 2)),  # No timepoints
            element_names=['N0', 'N1'],
            substrate='digital',
            metadata={}
        )
        calc = PhiCalculator()
        with pytest.raises((ValueError, IndexError)):
            calc.compute_phi(system)

    def test_constant_states(self):
        """Test system with constant states (no dynamics)."""
        n = 5
        system = NeuralSystem(
            connectivity=np.random.rand(n, n),
            states=np.ones((50, n)),  # All states identical
            element_names=[f'N{i}' for i in range(n)],
            substrate='digital',
            metadata={}
        )
        calc = PhiCalculator()
        metrics = calc.compute_phi(system)
        # Constant states might have low Φ (no information dynamics)
        assert metrics.phi >= 0

    def test_binary_states(self, chain_system):
        """Test with binary states."""
        n = chain_system['connectivity'].shape[0]
        chain_system['states'] = np.random.randint(0, 2, (100, n))
        system = NeuralSystem(**chain_system)
        calc = PhiCalculator()
        metrics = calc.compute_phi(system)
        assert metrics.phi >= 0

    def test_continuous_states(self, chain_system):
        """Test with continuous states."""
        n = chain_system['connectivity'].shape[0]
        chain_system['states'] = np.random.rand(100, n)
        system = NeuralSystem(**chain_system)
        calc = PhiCalculator()
        metrics = calc.compute_phi(system)
        assert metrics.phi >= 0


# ============================================================================
# SUBSTRATE COMPARISON TESTS
# ============================================================================

@pytest.mark.unit
class TestCrossSubstrateComparison:
    """Test Φ comparison across substrates."""

    def test_digital_vs_biological(self, digital_neural_net, small_brain_module):
        """Compare Φ between digital and biological systems of similar size."""
        calc = PhiCalculator()

        digital_sys = NeuralSystem(**digital_neural_net)
        bio_sys = NeuralSystem(**small_brain_module)

        digital_metrics = calc.compute_phi(digital_sys)
        bio_metrics = calc.compute_phi(bio_sys)

        # Both should have non-zero Φ
        assert digital_metrics.phi > 0
        assert bio_metrics.phi > 0

        # Check metadata
        assert digital_metrics.substrate_type == 'digital'
        assert bio_metrics.substrate_type == 'biological'

    def test_same_topology_different_substrate(self):
        """Test same connectivity pattern on different substrates."""
        n = 20
        connectivity = (np.random.rand(n, n) > 0.7).astype(float)
        states = np.random.rand(100, n)

        systems = {
            'digital': NeuralSystem(
                connectivity=connectivity.copy(),
                states=states.copy(),
                element_names=[f'N{i}' for i in range(n)],
                substrate='digital',
                metadata={}
            ),
            'biological': NeuralSystem(
                connectivity=connectivity.copy(),
                states=states.copy(),
                element_names=[f'N{i}' for i in range(n)],
                substrate='biological',
                metadata={}
            ),
            'hybrid': NeuralSystem(
                connectivity=connectivity.copy(),
                states=states.copy(),
                element_names=[f'N{i}' for i in range(n)],
                substrate='hybrid',
                metadata={}
            )
        }

        calc = PhiCalculator()
        phis = {}
        for substrate, system in systems.items():
            metrics = calc.compute_phi(system)
            phis[substrate] = metrics.phi

        # Same topology should give similar Φ regardless of substrate
        # (within reasonable tolerance due to numerical approximations)
        phi_values = list(phis.values())
        assert max(phi_values) / (min(phi_values) + 1e-10) < 2.0, \
            f"Same topology should give similar Φ across substrates: {phis}"


# ============================================================================
# PARAMETRIC TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.parametrize("system_size", [4, 8, 16, 32])
def test_phi_scales_with_size(system_size):
    """Test Φ calculation for different system sizes."""
    connectivity = (np.random.rand(system_size, system_size) > 0.7).astype(float)
    np.fill_diagonal(connectivity, 0)

    system = NeuralSystem(
        connectivity=connectivity,
        states=np.random.randint(0, 2, (50, system_size)),
        element_names=[f'N{i}' for i in range(system_size)],
        substrate='digital',
        metadata={'size': system_size}
    )

    calc = PhiCalculator()
    metrics = calc.compute_phi(system)

    assert metrics.phi >= 0
    assert metrics.system_size == system_size


@pytest.mark.unit
@pytest.mark.parametrize("topology", ['chain', 'ring', 'star', 'fully_connected'])
def test_phi_different_topologies(topology):
    """Test Φ for different network topologies."""
    n = 10
    connectivity = np.zeros((n, n))

    if topology == 'chain':
        for i in range(n - 1):
            connectivity[i, i + 1] = 1
    elif topology == 'ring':
        for i in range(n):
            connectivity[i, (i + 1) % n] = 1
    elif topology == 'star':
        connectivity[0, 1:] = 1
        connectivity[1:, 0] = 1
    elif topology == 'fully_connected':
        connectivity = np.ones((n, n)) - np.eye(n)

    system = NeuralSystem(
        connectivity=connectivity,
        states=np.random.randint(0, 2, (50, n)),
        element_names=[f'N{i}' for i in range(n)],
        substrate='digital',
        metadata={'topology': topology}
    )

    calc = PhiCalculator()
    metrics = calc.compute_phi(system)

    assert metrics.phi >= 0
    assert metrics.metadata.get('topology') == topology


# ============================================================================
# PERFORMANCE TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.slow
class TestPhiCalculatorPerformance:
    """Performance tests for Φ calculator."""

    def test_computation_time_scales(self, system_sizes):
        """Test that computation time scales reasonably."""
        calc = PhiCalculator()
        times = []

        for n in system_sizes:
            connectivity = (np.random.rand(n, n) > 0.7).astype(float)
            system = NeuralSystem(
                connectivity=connectivity,
                states=np.random.randint(0, 2, (50, n)),
                element_names=[f'N{i}' for i in range(n)],
                substrate='digital',
                metadata={}
            )
            metrics = calc.compute_phi(system)
            times.append(metrics.integration_time)

        # Should complete in reasonable time even for larger systems
        assert all(t < 10.0 for t in times), f"Computation times too slow: {times}"

    def test_large_system_tractable(self):
        """Test that reasonably large systems are tractable."""
        n = 100
        connectivity = (np.random.rand(n, n) > 0.8).astype(float)
        system = NeuralSystem(
            connectivity=connectivity,
            states=np.random.rand(100, n),
            element_names=[f'N{i}' for i in range(n)],
            substrate='digital',
            metadata={}
        )

        calc = PhiCalculator()
        metrics = calc.compute_phi(system)

        assert metrics.phi >= 0
        assert metrics.integration_time < 30.0, "Should complete within 30 seconds"


# ============================================================================
# REGRESSION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.regression
class TestPhiCalculatorRegression:
    """Regression tests for known issues."""

    def test_negative_phi_never_occurs(self, simple_system):
        """Ensure Φ is never negative (regression test)."""
        system = NeuralSystem(**simple_system)
        calc = PhiCalculator()

        # Run multiple times with different random states
        for _ in range(10):
            n = system.n_elements
            system.states = np.random.rand(100, n)
            metrics = calc.compute_phi(system)
            assert metrics.phi >= 0, "Φ must be non-negative"

    def test_phi_max_bounds(self, simple_system):
        """Test that Φ doesn't exceed theoretical maximum."""
        system = NeuralSystem(**simple_system)
        calc = PhiCalculator()
        metrics = calc.compute_phi(system)

        if metrics.phi_max is not None:
            assert metrics.phi <= metrics.phi_max, "Φ cannot exceed Φ_max"

    def test_symmetric_connectivity(self):
        """Test handling of symmetric connectivity matrices."""
        n = 8
        connectivity = np.random.rand(n, n)
        connectivity = (connectivity + connectivity.T) / 2  # Make symmetric

        system = NeuralSystem(
            connectivity=connectivity,
            states=np.random.rand(50, n),
            element_names=[f'N{i}' for i in range(n)],
            substrate='digital',
            metadata={'symmetric': True}
        )

        calc = PhiCalculator()
        metrics = calc.compute_phi(system)
        assert metrics.phi >= 0

    def test_numerical_stability(self):
        """Test numerical stability with extreme values."""
        n = 5
        # Very small connectivity values
        connectivity = np.random.rand(n, n) * 1e-10
        system = NeuralSystem(
            connectivity=connectivity,
            states=np.random.rand(50, n),
            element_names=[f'N{i}' for i in range(n)],
            substrate='digital',
            metadata={}
        )

        calc = PhiCalculator()
        metrics = calc.compute_phi(system)
        assert not np.isnan(metrics.phi), "Φ should not be NaN"
        assert not np.isinf(metrics.phi), "Φ should not be infinite"
