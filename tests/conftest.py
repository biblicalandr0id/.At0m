"""
Shared test fixtures for consciousness measurement framework.

Fixtures:
--------
- simple_system: Small 4-node test system
- elegans_mock: Mock C. elegans (302 neurons)
- digital_system: Digital substrate system
- quantum_system: Quantum substrate system
- biological_system: Biological neural system
- hybrid_system: Hybrid bio-digital system
"""

import pytest
import numpy as np
import sys
from pathlib import Path

# Add consciousness_measurement to path
sys.path.insert(0, str(Path(__file__).parent.parent / "consciousness_measurement" / "code"))


# ============================================================================
# BASIC TEST SYSTEMS
# ============================================================================

@pytest.fixture
def simple_system():
    """Simple 4-node test system with known properties."""
    return {
        'connectivity': np.array([
            [0, 1, 1, 0],
            [1, 0, 1, 1],
            [0, 1, 0, 1],
            [0, 1, 1, 0]
        ], dtype=float),
        'states': np.random.randint(0, 2, (100, 4)),
        'element_names': ['N0', 'N1', 'N2', 'N3'],
        'substrate': 'digital',
        'metadata': {'type': 'test_system', 'size': 4}
    }


@pytest.fixture
def isolated_system():
    """System with no connections (should have Φ ≈ 0)."""
    n = 5
    return {
        'connectivity': np.zeros((n, n)),
        'states': np.random.randint(0, 2, (50, n)),
        'element_names': [f'N{i}' for i in range(n)],
        'substrate': 'digital',
        'metadata': {'type': 'isolated', 'expected_phi': 0.0}
    }


@pytest.fixture
def fully_connected_system():
    """Fully connected system (high Φ expected)."""
    n = 6
    connectivity = np.ones((n, n)) - np.eye(n)  # All-to-all except self
    return {
        'connectivity': connectivity,
        'states': np.random.randint(0, 2, (100, n)),
        'element_names': [f'N{i}' for i in range(n)],
        'substrate': 'digital',
        'metadata': {'type': 'fully_connected', 'expected_phi': 'high'}
    }


@pytest.fixture
def chain_system():
    """Linear chain topology (low-medium Φ)."""
    n = 8
    connectivity = np.zeros((n, n))
    for i in range(n - 1):
        connectivity[i, i + 1] = 1
        connectivity[i + 1, i] = 1  # Bidirectional
    return {
        'connectivity': connectivity,
        'states': np.random.randint(0, 2, (100, n)),
        'element_names': [f'N{i}' for i in range(n)],
        'substrate': 'digital',
        'metadata': {'type': 'chain', 'expected_phi': 'medium'}
    }


# ============================================================================
# BIOLOGICAL SYSTEMS
# ============================================================================

@pytest.fixture
def elegans_mock():
    """Mock C. elegans connectome (simplified 302 neurons)."""
    n = 302
    # Small-world connectivity (characteristic of real C. elegans)
    p_local = 0.3  # Local connection probability
    p_random = 0.05  # Long-range connection probability

    connectivity = np.zeros((n, n))

    # Local connections
    for i in range(n):
        for j in range(max(0, i - 5), min(n, i + 6)):
            if i != j and np.random.rand() < p_local:
                connectivity[i, j] = 1

    # Random long-range connections
    for i in range(n):
        for j in range(n):
            if i != j and np.random.rand() < p_random:
                connectivity[i, j] = 1

    states = np.random.rand(100, n)  # Continuous states (firing rates)

    return {
        'connectivity': connectivity,
        'states': states,
        'element_names': [f'Neuron_{i}' for i in range(n)],
        'substrate': 'biological',
        'metadata': {
            'organism': 'C. elegans',
            'n_neurons': n,
            'connectivity_density': connectivity.sum() / (n * n)
        }
    }


@pytest.fixture
def small_brain_module():
    """Small brain module (e.g., cortical column analogue, 100 neurons)."""
    n = 100
    # Scale-free connectivity (power law)
    connectivity = np.zeros((n, n))

    for i in range(n):
        # Number of connections follows power law
        k = int(np.random.pareto(2) * 2) + 2
        k = min(k, n - 1)
        targets = np.random.choice([j for j in range(n) if j != i], k, replace=False)
        connectivity[i, targets] = 1

    return {
        'connectivity': connectivity,
        'states': np.random.rand(200, n),
        'element_names': [f'Cortex_{i}' for i in range(n)],
        'substrate': 'biological',
        'metadata': {'type': 'cortical_column', 'scale_free': True}
    }


# ============================================================================
# DIGITAL SYSTEMS
# ============================================================================

@pytest.fixture
def digital_neural_net():
    """Digital neural network (50 nodes)."""
    n = 50
    # Layered architecture: 20 input, 20 hidden, 10 output
    connectivity = np.zeros((n, n))

    # Input -> Hidden
    connectivity[0:20, 20:40] = np.random.rand(20, 20) > 0.5
    # Hidden -> Output
    connectivity[20:40, 40:50] = np.random.rand(20, 10) > 0.5
    # Recurrent connections in hidden layer
    connectivity[20:40, 20:40] = np.random.rand(20, 20) > 0.8

    return {
        'connectivity': connectivity,
        'states': np.random.rand(150, n),
        'element_names': [f'Unit_{i}' for i in range(n)],
        'substrate': 'digital',
        'metadata': {'architecture': 'feedforward+recurrent', 'layers': 3}
    }


# ============================================================================
# QUANTUM SYSTEMS
# ============================================================================

@pytest.fixture
def quantum_system():
    """Quantum system (10 qubits with entanglement)."""
    n = 10
    # Quantum systems have complex-valued connectivity
    connectivity = (np.random.rand(n, n) + 1j * np.random.rand(n, n)) / 2
    connectivity = (connectivity + connectivity.conj().T) / 2  # Hermitian

    # Quantum states are probability amplitudes
    states = np.random.rand(50, n) + 1j * np.random.rand(50, n)
    states = states / np.linalg.norm(states, axis=1, keepdims=True)  # Normalize

    return {
        'connectivity': connectivity,
        'states': states,
        'element_names': [f'Qubit_{i}' for i in range(n)],
        'substrate': 'quantum',
        'metadata': {'qubit_count': n, 'entanglement': True}
    }


# ============================================================================
# HYBRID SYSTEMS
# ============================================================================

@pytest.fixture
def hybrid_bio_digital():
    """Hybrid biological-digital system."""
    n_bio = 20
    n_digital = 30
    n = n_bio + n_digital

    connectivity = np.zeros((n, n))
    # Biological connections
    connectivity[0:n_bio, 0:n_bio] = np.random.rand(n_bio, n_bio) > 0.7
    # Digital connections
    connectivity[n_bio:n, n_bio:n] = np.random.rand(n_digital, n_digital) > 0.6
    # Bio-digital interface
    connectivity[0:n_bio, n_bio:n] = np.random.rand(n_bio, n_digital) > 0.85
    connectivity[n_bio:n, 0:n_bio] = np.random.rand(n_digital, n_bio) > 0.85

    states = np.random.rand(100, n)

    return {
        'connectivity': connectivity,
        'states': states,
        'element_names': [f'Bio_{i}' for i in range(n_bio)] + [f'Dig_{i}' for i in range(n_digital)],
        'substrate': 'hybrid',
        'metadata': {
            'n_biological': n_bio,
            'n_digital': n_digital,
            'interface_density': connectivity[0:n_bio, n_bio:n].sum() / (n_bio * n_digital)
        }
    }


# ============================================================================
# SUBSTRATE SPECIFICATIONS
# ============================================================================

@pytest.fixture
def biological_substrate_spec():
    """Standard biological neural substrate constraints."""
    from substrate_translator import SubstrateType, SubstrateConstraints
    return SubstrateConstraints(
        substrate_type=SubstrateType.NEURAL_BIOLOGICAL,
        max_elements=10**11,  # ~100 billion neurons
        min_integration_time=0.001,  # 1ms (spike)
        max_integration_time=10.0,  # 10s (slow oscillations)
        connection_density=0.0001,  # Sparse
        state_dimensions=1,  # Firing rate
        noise_level=0.1,
        energy_cost_per_bit=1e-15,  # ~fJ per spike
        decoherence_time=None,
        temperature_range=(273, 310),  # 0-37°C
        spatial_scalability=0.7,
        temporal_stability=0.8,
        reversibility=0.2  # Mostly irreversible
    )


@pytest.fixture
def digital_substrate_spec():
    """Standard digital silicon substrate constraints."""
    from substrate_translator import SubstrateType, SubstrateConstraints
    return SubstrateConstraints(
        substrate_type=SubstrateType.SILICON_DIGITAL,
        max_elements=10**12,  # Trillion transistors
        min_integration_time=1e-9,  # 1ns (GHz clock)
        max_integration_time=1.0,  # 1s (reasonable timeout)
        connection_density=0.01,
        state_dimensions=64,  # 64-bit floats
        noise_level=0.01,
        energy_cost_per_bit=1e-12,  # pJ per operation
        decoherence_time=None,
        temperature_range=(223, 373),  # -50 to 100°C
        spatial_scalability=0.95,  # Highly scalable
        temporal_stability=0.99,
        reversibility=1.0  # Fully reversible
    )


@pytest.fixture
def quantum_substrate_spec():
    """Standard quantum qubit substrate constraints."""
    from substrate_translator import SubstrateType, SubstrateConstraints
    return SubstrateConstraints(
        substrate_type=SubstrateType.QUANTUM_QUBIT,
        max_elements=1000,  # Current technology ~100s of qubits
        min_integration_time=1e-9,  # Nanoseconds
        max_integration_time=1e-4,  # 100μs decoherence
        connection_density=1.0,  # Fully entangleable
        state_dimensions=2,  # Qubit (complex 2D)
        noise_level=0.05,
        energy_cost_per_bit=1e-18,  # aJ
        decoherence_time=1e-4,  # 100μs
        temperature_range=(0.01, 4),  # Near absolute zero
        spatial_scalability=0.3,  # Hard to scale
        temporal_stability=0.4,  # Decoherence issues
        reversibility=1.0  # Quantum operations are reversible
    )


# ============================================================================
# PARAMETRIC TEST DATA
# ============================================================================

@pytest.fixture
def system_sizes():
    """Different system sizes for parametric testing."""
    return [4, 8, 16, 32, 64]


@pytest.fixture
def phi_test_cases():
    """Known Φ test cases for validation."""
    return [
        {
            'name': 'isolated_units',
            'connectivity': np.zeros((5, 5)),
            'expected_phi': 0.0,
            'tolerance': 0.001
        },
        {
            'name': 'xor_gate',
            'connectivity': np.array([[0, 1], [1, 0]]),
            'expected_phi': 0.1,  # Small but non-zero
            'tolerance': 0.05
        },
        {
            'name': 'triangle',
            'connectivity': np.array([
                [0, 1, 1],
                [1, 0, 1],
                [1, 1, 0]
            ]),
            'expected_phi': 0.5,  # Moderate integration
            'tolerance': 0.2
        }
    ]


# ============================================================================
# TEMPORARY DIRECTORIES
# ============================================================================

@pytest.fixture
def temp_output_dir(tmp_path):
    """Temporary directory for test outputs."""
    output_dir = tmp_path / "consciousness_test_output"
    output_dir.mkdir()
    return output_dir


# ============================================================================
# RANDOM SEED CONTROL
# ============================================================================

@pytest.fixture(autouse=True)
def reset_random_seed():
    """Reset random seed before each test for reproducibility."""
    np.random.seed(42)
    yield
    # Cleanup if needed


# ============================================================================
# SKIP MARKERS FOR OPTIONAL DEPENDENCIES
# ============================================================================

@pytest.fixture
def check_gpu_available():
    """Check if GPU/CUDA is available."""
    try:
        import cupy
        return True
    except ImportError:
        pytest.skip("GPU/CUDA not available")


@pytest.fixture
def check_pyphi_available():
    """Check if PyPhi is installed (for exact validation)."""
    try:
        import pyphi
        return True
    except ImportError:
        pytest.skip("PyPhi not installed")
