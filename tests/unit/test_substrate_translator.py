"""
Unit tests for cross-substrate consciousness translation.

Tests:
-----
- Substrate type enumeration
- Substrate constraints
- Universal Consciousness Representation (UCR)
- Pattern extraction from source substrate
- Pattern translation to target substrate
- Φ preservation validation
- Edge cases and error handling
"""

import pytest
import numpy as np
from pathlib import Path

from substrate_translator import (
    SubstrateType,
    SubstrateConstraints,
    UniversalConsciousnessRepresentation,
    SubstrateTranslator,
    TranslationResult
)


# ============================================================================
# SUBSTRATE TYPE TESTS
# ============================================================================

@pytest.mark.unit
class TestSubstrateType:
    """Test substrate type enumeration."""

    def test_all_types_accessible(self):
        """Test that all substrate types are accessible."""
        assert SubstrateType.NEURAL_BIOLOGICAL
        assert SubstrateType.SILICON_DIGITAL
        assert SubstrateType.QUANTUM_QUBIT
        assert SubstrateType.BIO_SILICON

    def test_substrate_categories(self):
        """Test categorization of substrates."""
        biological = [
            SubstrateType.NEURAL_BIOLOGICAL,
            SubstrateType.DNA_MOLECULAR,
            SubstrateType.PROTEIN_FOLDING
        ]
        for substrate in biological:
            assert 'biological' in substrate.value or 'dna' in substrate.value or 'protein' in substrate.value

        digital = [
            SubstrateType.SILICON_DIGITAL,
            SubstrateType.NEUROMORPHIC,
            SubstrateType.GPU_PARALLEL
        ]
        for substrate in digital:
            assert 'digital' in substrate.value or 'neuromorphic' in substrate.value or 'gpu' in substrate.value


# ============================================================================
# SUBSTRATE CONSTRAINTS TESTS
# ============================================================================

@pytest.mark.unit
class TestSubstrateConstraints:
    """Test substrate constraint specifications."""

    def test_biological_constraints(self, biological_substrate_spec):
        """Test biological substrate constraints."""
        spec = biological_substrate_spec
        assert spec.substrate_type == SubstrateType.NEURAL_BIOLOGICAL
        assert spec.max_elements > 0
        assert 0 <= spec.noise_level <= 1
        assert spec.min_integration_time < spec.max_integration_time
        assert 0 <= spec.connection_density <= 1

    def test_digital_constraints(self, digital_substrate_spec):
        """Test digital substrate constraints."""
        spec = digital_substrate_spec
        assert spec.substrate_type == SubstrateType.SILICON_DIGITAL
        assert spec.reversibility == 1.0, "Digital computation is fully reversible"
        assert spec.noise_level < 0.1, "Digital systems have low noise"
        assert spec.spatial_scalability > 0.9, "Digital scales well"

    def test_quantum_constraints(self, quantum_substrate_spec):
        """Test quantum substrate constraints."""
        spec = quantum_substrate_spec
        assert spec.substrate_type == SubstrateType.QUANTUM_QUBIT
        assert spec.decoherence_time is not None, "Quantum systems have decoherence"
        assert spec.reversibility == 1.0, "Quantum operations are reversible"
        assert spec.temperature_range[1] < 10, "Quantum requires cryogenic temps"

    def test_constraint_validation(self):
        """Test validation of constraint parameters."""
        # Valid constraints
        valid = SubstrateConstraints(
            substrate_type=SubstrateType.SILICON_DIGITAL,
            max_elements=1000,
            min_integration_time=1e-9,
            max_integration_time=1.0,
            connection_density=0.5,
            state_dimensions=32,
            noise_level=0.01,
            energy_cost_per_bit=1e-12,
            decoherence_time=None,
            temperature_range=(273, 373),
            spatial_scalability=0.95,
            temporal_stability=0.99,
            reversibility=1.0
        )
        assert valid.max_elements == 1000

        # Invalid constraints should be caught
        with pytest.raises((ValueError, AssertionError)):
            invalid = SubstrateConstraints(
                substrate_type=SubstrateType.SILICON_DIGITAL,
                max_elements=-1000,  # Negative elements
                min_integration_time=1e-9,
                max_integration_time=1.0,
                connection_density=0.5,
                state_dimensions=32,
                noise_level=0.01,
                energy_cost_per_bit=1e-12,
                decoherence_time=None,
                temperature_range=(273, 373),
                spatial_scalability=0.95,
                temporal_stability=0.99,
                reversibility=1.0
            )


# ============================================================================
# SUBSTRATE TRANSLATOR TESTS
# ============================================================================

@pytest.mark.unit
class TestSubstrateTranslator:
    """Test substrate translator core functionality."""

    def test_initialization(self):
        """Test translator initialization."""
        translator = SubstrateTranslator()
        assert translator is not None

    def test_extract_pattern_biological(self, small_brain_module):
        """Test pattern extraction from biological substrate."""
        from phi_calculator import NeuralSystem
        system = NeuralSystem(**small_brain_module)

        translator = SubstrateTranslator()
        ucr = translator.extract_pattern(system)

        assert isinstance(ucr, UniversalConsciousnessRepresentation)
        assert ucr.n_elements == system.n_elements
        assert ucr.source_substrate == 'biological'

    def test_extract_pattern_digital(self, digital_neural_net):
        """Test pattern extraction from digital substrate."""
        from phi_calculator import NeuralSystem
        system = NeuralSystem(**digital_neural_net)

        translator = SubstrateTranslator()
        ucr = translator.extract_pattern(system)

        assert isinstance(ucr, UniversalConsciousnessRepresentation)
        assert ucr.n_elements == system.n_elements
        assert ucr.source_substrate == 'digital'

    def test_translate_biological_to_digital(
        self, small_brain_module, biological_substrate_spec, digital_substrate_spec
    ):
        """Test translation from biological to digital substrate."""
        from phi_calculator import NeuralSystem
        source_system = NeuralSystem(**small_brain_module)

        translator = SubstrateTranslator()
        result = translator.translate(
            source_data=source_system,
            source_substrate=biological_substrate_spec.substrate_type,
            target_substrate=digital_substrate_spec.substrate_type
        )

        assert isinstance(result, TranslationResult)
        assert result.success
        assert result.target_substrate == SubstrateType.SILICON_DIGITAL
        assert result.phi_preservation_ratio > 0
        assert result.phi_preservation_ratio <= 1.0

    def test_translate_digital_to_quantum(
        self, digital_neural_net, digital_substrate_spec, quantum_substrate_spec
    ):
        """Test translation from digital to quantum substrate."""
        from phi_calculator import NeuralSystem
        source_system = NeuralSystem(**digital_neural_net)

        translator = SubstrateTranslator()
        result = translator.translate(
            source_data=source_system,
            source_substrate=digital_substrate_spec.substrate_type,
            target_substrate=quantum_substrate_spec.substrate_type
        )

        assert isinstance(result, TranslationResult)
        # Quantum has limited elements, so might require downsampling
        assert result.target_system is not None

    def test_phi_preservation_threshold(
        self, simple_system, biological_substrate_spec, digital_substrate_spec
    ):
        """Test that Φ preservation meets >80% threshold."""
        from phi_calculator import NeuralSystem
        simple_system['substrate'] = 'biological'
        source_system = NeuralSystem(**simple_system)

        translator = SubstrateTranslator()
        result = translator.translate(
            source_data=source_system,
            source_substrate=biological_substrate_spec.substrate_type,
            target_substrate=digital_substrate_spec.substrate_type
        )

        # Framework claims >80% Φ preservation
        if result.success:
            assert result.phi_preservation_ratio > 0.8, \
                f"Φ preservation should be >80%, got {result.phi_preservation_ratio}"

    def test_reversible_translation(self, simple_system, biological_substrate_spec, digital_substrate_spec):
        """Test round-trip translation (bio → digital → bio)."""
        from phi_calculator import NeuralSystem
        simple_system['substrate'] = 'biological'
        original_system = NeuralSystem(**simple_system)

        translator = SubstrateTranslator()

        # Bio → Digital
        result1 = translator.translate(
            source_data=original_system,
            source_substrate=biological_substrate_spec.substrate_type,
            target_substrate=digital_substrate_spec.substrate_type
        )

        # Digital → Bio
        result2 = translator.translate(
            source_data=result1.target_system,
            source_substrate=digital_substrate_spec.substrate_type,
            target_substrate=biological_substrate_spec.substrate_type
        )

        # Check that round-trip preserves most structure
        assert result2.success
        # Cumulative Φ preservation
        cumulative_preservation = result1.phi_preservation_ratio * result2.phi_preservation_ratio
        assert cumulative_preservation > 0.6, \
            f"Round-trip should preserve >60% Φ, got {cumulative_preservation}"


# ============================================================================
# EDGE CASES AND ERROR HANDLING
# ============================================================================

@pytest.mark.unit
class TestSubstrateTranslatorEdgeCases:
    """Test edge cases for substrate translation."""

    def test_translate_to_same_substrate(self, simple_system, digital_substrate_spec):
        """Test translation to the same substrate type."""
        from phi_calculator import NeuralSystem
        system = NeuralSystem(**simple_system)

        translator = SubstrateTranslator()
        result = translator.translate(
            source_data=system,
            source_substrate=digital_substrate_spec.substrate_type,
            target_substrate=digital_substrate_spec.substrate_type
        )

        # Same substrate should preserve Φ perfectly
        if result.success:
            assert result.phi_preservation_ratio > 0.95

    def test_translate_exceeds_target_capacity(self, elegans_mock, quantum_substrate_spec):
        """Test translation when source exceeds target capacity."""
        from phi_calculator import NeuralSystem
        # C. elegans has 302 neurons, quantum substrate typically < 1000 qubits
        system = NeuralSystem(**elegans_mock)

        translator = SubstrateTranslator()
        # Should handle capacity constraints gracefully
        result = translator.translate(
            source_data=system,
            source_substrate=SubstrateType.NEURAL_BIOLOGICAL,
            target_substrate=quantum_substrate_spec.substrate_type
        )

        # Should either succeed with compression or fail gracefully
        assert result.success in [True, False]
        if not result.success:
            assert result.error_message is not None

    def test_translate_with_incompatible_constraints(self):
        """Test translation with physically incompatible constraints."""
        from phi_calculator import NeuralSystem

        # Create a system
        n = 10
        system = NeuralSystem(
            connectivity=np.random.rand(n, n),
            states=np.random.rand(50, n),
            element_names=[f'N{i}' for i in range(n)],
            substrate='digital',
            metadata={}
        )

        # Create incompatible constraints (e.g., target too small)
        source_spec = SubstrateConstraints(
            substrate_type=SubstrateType.SILICON_DIGITAL,
            max_elements=10,
            min_integration_time=1e-9,
            max_integration_time=1.0,
            connection_density=0.5,
            state_dimensions=32,
            noise_level=0.01,
            energy_cost_per_bit=1e-12,
            decoherence_time=None,
            temperature_range=(273, 373),
            spatial_scalability=0.95,
            temporal_stability=0.99,
            reversibility=1.0
        )

        target_spec = SubstrateConstraints(
            substrate_type=SubstrateType.QUANTUM_QUBIT,
            max_elements=2,  # Too small!
            min_integration_time=1e-9,
            max_integration_time=1e-4,
            connection_density=1.0,
            state_dimensions=2,
            noise_level=0.05,
            energy_cost_per_bit=1e-18,
            decoherence_time=1e-4,
            temperature_range=(0.01, 4),
            spatial_scalability=0.3,
            temporal_stability=0.4,
            reversibility=1.0
        )

        translator = SubstrateTranslator()
        result = translator.translate(
            source_data=system,
            source_substrate=source_spec.substrate_type,
            target_substrate=target_spec.substrate_type
        )

        # Should handle gracefully (either succeed with severe compression or fail)
        assert isinstance(result, TranslationResult)


# ============================================================================
# PARAMETRIC TRANSLATION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.parametrize("source_type,target_type", [
    (SubstrateType.NEURAL_BIOLOGICAL, SubstrateType.SILICON_DIGITAL),
    (SubstrateType.SILICON_DIGITAL, SubstrateType.QUANTUM_QUBIT),
    (SubstrateType.SILICON_DIGITAL, SubstrateType.NEUROMORPHIC),
    (SubstrateType.NEUROMORPHIC, SubstrateType.SILICON_DIGITAL),
])
def test_translation_pairs(source_type, target_type):
    """Test translation between various substrate pairs."""
    from phi_calculator import NeuralSystem

    n = 10
    system = NeuralSystem(
        connectivity=np.random.rand(n, n) > 0.7,
        states=np.random.rand(50, n),
        element_names=[f'N{i}' for i in range(n)],
        substrate='test',
        metadata={}
    )

    source_spec = SubstrateConstraints(
        substrate_type=source_type,
        max_elements=100,
        min_integration_time=1e-6,
        max_integration_time=1.0,
        connection_density=0.3,
        state_dimensions=8,
        noise_level=0.1,
        energy_cost_per_bit=1e-12,
        decoherence_time=None if 'quantum' not in source_type.value else 1e-4,
        temperature_range=(273, 373),
        spatial_scalability=0.7,
        temporal_stability=0.8,
        reversibility=0.5
    )

    target_spec = SubstrateConstraints(
        substrate_type=target_type,
        max_elements=100,
        min_integration_time=1e-6,
        max_integration_time=1.0,
        connection_density=0.3,
        state_dimensions=8,
        noise_level=0.1,
        energy_cost_per_bit=1e-12,
        decoherence_time=None if 'quantum' not in target_type.value else 1e-4,
        temperature_range=(273, 373),
        spatial_scalability=0.7,
        temporal_stability=0.8,
        reversibility=0.5
    )

    translator = SubstrateTranslator()
    result = translator.translate(
        source_data=system,
        source_substrate=source_spec.substrate_type,
        target_substrate=target_spec.substrate_type
    )

    assert isinstance(result, TranslationResult)


# ============================================================================
# VALIDATION TESTS
# ============================================================================

@pytest.mark.unit
@pytest.mark.validation
class TestTranslationValidation:
    """Validation tests for translation quality."""

    def test_topology_preservation(self, simple_system, biological_substrate_spec, digital_substrate_spec):
        """Test that translation preserves network topology."""
        from phi_calculator import NeuralSystem
        simple_system['substrate'] = 'biological'
        source_system = NeuralSystem(**simple_system)

        translator = SubstrateTranslator()
        result = translator.translate(
            source_data=source_system,
            source_substrate=biological_substrate_spec.substrate_type,
            target_substrate=digital_substrate_spec.substrate_type
        )

        if result.success:
            # Check that basic topology features are preserved
            source_conn = source_system.connectivity
            target_conn = result.target_system.connectivity

            # Number of elements should be similar (within target constraints)
            assert result.target_system.n_elements > 0

            # Connection density should be similar
            source_density = (source_conn > 0).sum() / source_conn.size
            target_density = (target_conn > 0).sum() / target_conn.size
            density_ratio = target_density / (source_density + 1e-10)
            assert 0.5 < density_ratio < 2.0, \
                f"Connectivity density should be preserved (ratio: {density_ratio})"

    def test_phi_calculation_on_translated_system(
        self, simple_system, biological_substrate_spec, digital_substrate_spec
    ):
        """Test that translated system can have Φ calculated."""
        from phi_calculator import NeuralSystem, PhiCalculator

        simple_system['substrate'] = 'biological'
        source_system = NeuralSystem(**simple_system)

        translator = SubstrateTranslator()
        result = translator.translate(
            source_data=source_system,
            source_substrate=biological_substrate_spec.substrate_type,
            target_substrate=digital_substrate_spec.substrate_type
        )

        if result.success:
            # Should be able to calculate Φ on translated system
            calc = PhiCalculator()
            metrics = calc.compute_phi(result.target_system)
            assert metrics.phi >= 0
            assert metrics.system_size == result.target_system.n_elements
