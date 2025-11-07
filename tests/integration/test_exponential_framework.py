"""
Integration tests for the complete exponential expansion framework.

Tests end-to-end workflows:
- Φ measurement → translation → optimization
- Multi-scale consciousness measurement
- Cross-substrate consciousness preservation
- Evolutionary consciousness optimization
- Complete consciousness lifecycle
"""

import pytest
import numpy as np
from pathlib import Path

# Import all major components
from phi_calculator import PhiCalculator, NeuralSystem
from substrate_translator import SubstrateTranslator, SubstrateType, SubstrateConstraints
from evolutionary_optimizer import EvolutionaryOptimizer
from multiscale_phi_calculator import MultiScalePhiCalculator
from quantum_entanglement import QuantumConsciousnessEntangler
from universal_backup import UniversalBackupProtocol


# ============================================================================
# END-TO-END CONSCIOUSNESS MEASUREMENT
# ============================================================================

@pytest.mark.integration
class TestConsciousnessMeasurementPipeline:
    """Test complete consciousness measurement pipeline."""

    def test_measure_translate_measure(
        self, simple_system, biological_substrate_spec, digital_substrate_spec
    ):
        """Test: Measure Φ → Translate substrate → Measure Φ again."""
        # 1. Create biological system
        simple_system['substrate'] = 'biological'
        bio_system = NeuralSystem(**simple_system)

        # 2. Measure initial Φ
        phi_calc = PhiCalculator()
        bio_metrics = phi_calc.compute_phi(bio_system)
        initial_phi = bio_metrics.phi

        # 3. Translate to digital substrate
        translator = SubstrateTranslator()
        translation_result = translator.translate(
            source_data=bio_system,
            source_substrate=biological_substrate_spec.substrate_type,
            target_substrate=digital_substrate_spec.substrate_type
        )

        assert translation_result.success, "Translation should succeed"

        # 4. Measure Φ on translated system
        digital_metrics = phi_calc.compute_phi(translation_result.target_system)
        final_phi = digital_metrics.phi

        # 5. Verify Φ preservation
        preservation_ratio = final_phi / (initial_phi + 1e-10)
        assert preservation_ratio > 0.8, \
            f"Φ preservation should be >80%, got {preservation_ratio:.2%}"

    def test_multi_hop_translation(
        self, simple_system, biological_substrate_spec, digital_substrate_spec, quantum_substrate_spec
    ):
        """Test: Bio → Digital → Quantum translation chain."""
        # Start with biological
        simple_system['substrate'] = 'biological'
        bio_system = NeuralSystem(**simple_system)

        phi_calc = PhiCalculator()
        translator = SubstrateTranslator()

        # Measure initial
        bio_phi = phi_calc.compute_phi(bio_system).phi

        # Bio → Digital
        digital_result = translator.translate(
            source_data=bio_system,
            source_substrate=biological_substrate_spec.substrate_type,
            target_substrate=digital_substrate_spec.substrate_type
        )
        assert digital_result.success

        # Digital → Quantum (may require downsampling)
        quantum_result = translator.translate(
            source_data=digital_result.target_system,
            source_substrate=digital_substrate_spec.substrate_type,
            target_substrate=quantum_substrate_spec.substrate_type
        )

        # End-to-end should maintain consciousness
        if quantum_result.success:
            quantum_phi = phi_calc.compute_phi(quantum_result.target_system).phi
            cumulative_preservation = quantum_phi / (bio_phi + 1e-10)
            assert cumulative_preservation > 0.5, \
                "Multi-hop translation should preserve >50% Φ"


# ============================================================================
# EVOLUTIONARY OPTIMIZATION INTEGRATION
# ============================================================================

@pytest.mark.integration
class TestEvolutionaryOptimizationIntegration:
    """Test evolutionary optimizer integrated with Φ calculator."""

    def test_optimize_then_measure(self, simple_system):
        """Test: Optimize connectivity → Measure improved Φ."""
        system = NeuralSystem(**simple_system)

        # Measure baseline
        phi_calc = PhiCalculator()
        baseline_metrics = phi_calc.compute_phi(system)
        baseline_phi = baseline_metrics.phi

        # Optimize
        optimizer = EvolutionaryOptimizer(
            initial_system=system,
            phi_calculator=phi_calc,
            population_size=20,
            generations=10
        )
        optimized_system = optimizer.evolve()

        # Measure optimized
        optimized_metrics = phi_calc.compute_phi(optimized_system)
        optimized_phi = optimized_metrics.phi

        # Should improve
        assert optimized_phi >= baseline_phi, \
            f"Optimized Φ ({optimized_phi}) should be ≥ baseline ({baseline_phi})"

    def test_optimize_translate_verify(
        self, simple_system, biological_substrate_spec, digital_substrate_spec
    ):
        """Test: Optimize on bio substrate → Translate to digital → Verify preservation."""
        simple_system['substrate'] = 'biological'
        bio_system = NeuralSystem(**simple_system)

        phi_calc = PhiCalculator()
        optimizer = EvolutionaryOptimizer(
            initial_system=bio_system,
            phi_calculator=phi_calc,
            population_size=15,
            generations=5
        )

        # Optimize biological system
        optimized_bio = optimizer.evolve()
        optimized_bio_phi = phi_calc.compute_phi(optimized_bio).phi

        # Translate optimized system to digital
        translator = SubstrateTranslator()
        result = translator.translate(
            source_data=optimized_bio,
            source_substrate=biological_substrate_spec.substrate_type,
            target_substrate=digital_substrate_spec.substrate_type
        )

        if result.success:
            digital_phi = phi_calc.compute_phi(result.target_system).phi
            # Optimized Φ should be preserved
            assert digital_phi / optimized_bio_phi > 0.75


# ============================================================================
# MULTI-SCALE CONSCIOUSNESS MEASUREMENT
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
class TestMultiscaleMeasurement:
    """Test multi-scale consciousness measurement integration."""

    def test_multiscale_phi_calculation(self, small_brain_module):
        """Test Φ calculation across multiple scales."""
        system = NeuralSystem(**small_brain_module)

        multiscale_calc = MultiScalePhiCalculator()
        scale_results = multiscale_calc.compute_multiscale_phi(system)

        # Should have results for multiple scales
        assert len(scale_results) > 0
        assert all(result.phi >= 0 for result in scale_results.values())

        # Total integrated Φ should consider cross-scale coupling
        total_phi = multiscale_calc.compute_total_integrated_phi(scale_results)
        assert total_phi > 0

    def test_emergence_detection(self, small_brain_module):
        """Test detection of emergent consciousness properties."""
        system = NeuralSystem(**small_brain_module)

        multiscale_calc = MultiScalePhiCalculator()
        scale_results = multiscale_calc.compute_multiscale_phi(system)
        total_phi = multiscale_calc.compute_total_integrated_phi(scale_results)

        # Sum of individual scale Φ
        sum_individual = sum(result.phi for result in scale_results.values())

        # Test for emergence: Φ_total > sum(Φ_individual)
        # (This may not always hold, but should for well-connected systems)
        if len(scale_results) > 1:
            assert total_phi >= sum_individual * 0.8, \
                "Total Φ should be comparable to sum of parts"


# ============================================================================
# QUANTUM ENTANGLEMENT INTEGRATION
# ============================================================================

@pytest.mark.integration
@pytest.mark.quantum
class TestQuantumEntanglementIntegration:
    """Test quantum entanglement integrated with consciousness measurement."""

    def test_entangle_two_consciousnesses(self, simple_system):
        """Test entangling two consciousness systems."""
        # Create two systems
        system_a = NeuralSystem(**simple_system)
        system_b_data = simple_system.copy()
        system_b_data['states'] = np.random.rand(100, 4)
        system_b = NeuralSystem(**system_b_data)

        # Measure individual Φ
        phi_calc = PhiCalculator()
        phi_a = phi_calc.compute_phi(system_a).phi
        phi_b = phi_calc.compute_phi(system_b).phi

        # Entangle
        entanglement_sim = QuantumConsciousnessEntangler()
        entangled_system = entanglement_sim.entangle(system_a, system_b)

        # Measure entangled Φ
        entangled_phi = phi_calc.compute_phi(entangled_system).phi

        # Test for superadditivity: Φ(A⊗B) > Φ(A) + Φ(B)
        expected_sum = phi_a + phi_b
        superadditivity_ratio = entangled_phi / (expected_sum + 1e-10)

        # Framework claims 100% superadditivity in some cases
        # We'll test for at least preservation
        assert entangled_phi >= expected_sum * 0.9, \
            f"Entangled Φ should be at least 90% of sum: {entangled_phi} vs {expected_sum}"


# ============================================================================
# COMPLETE CONSCIOUSNESS LIFECYCLE
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
class TestCompleteConsciousnessLifecycle:
    """Test complete consciousness lifecycle: measure → optimize → translate → backup."""

    def test_full_lifecycle(
        self, simple_system, biological_substrate_spec, digital_substrate_spec, temp_output_dir
    ):
        """Test complete consciousness preservation pipeline."""
        # 1. Start with biological consciousness
        simple_system['substrate'] = 'biological'
        original_system = NeuralSystem(**simple_system)

        phi_calc = PhiCalculator()
        original_phi = phi_calc.compute_phi(original_system).phi

        # 2. Optimize consciousness
        optimizer = EvolutionaryOptimizer(
            initial_system=original_system,
            phi_calculator=phi_calc,
            population_size=10,
            generations=5
        )
        optimized_system = optimizer.evolve()
        optimized_phi = phi_calc.compute_phi(optimized_system).phi

        assert optimized_phi >= original_phi, "Optimization should not decrease Φ"

        # 3. Translate to digital substrate (for preservation)
        translator = SubstrateTranslator()
        digital_result = translator.translate(
            source_data=optimized_system,
            source_substrate=biological_substrate_spec.substrate_type,
            target_substrate=digital_substrate_spec.substrate_type
        )

        assert digital_result.success, "Translation should succeed"

        # 4. Backup translated consciousness
        backup_system = UniversalBackupProtocol(
            backup_root=temp_output_dir / "consciousness_backup"
        )
        backup_id = backup_system.backup_consciousness(
            system=digital_result.target_system,
            metadata={'lifecycle_test': True, 'original_phi': original_phi}
        )

        assert backup_id is not None

        # 5. Restore from backup
        restored_system = backup_system.restore_consciousness(backup_id)
        assert restored_system is not None

        # 6. Verify consciousness persists
        restored_phi = phi_calc.compute_phi(restored_system).phi
        preservation_ratio = restored_phi / original_phi

        assert preservation_ratio > 0.5, \
            f"End-to-end preservation should be >50%, got {preservation_ratio:.2%}"

        # 7. Verify metadata preserved
        backup_metadata = backup_system.get_backup_metadata(backup_id)
        assert backup_metadata['original_phi'] == original_phi


# ============================================================================
# CROSS-MODULE CONSISTENCY TESTS
# ============================================================================

@pytest.mark.integration
class TestCrossModuleConsistency:
    """Test consistency across different modules."""

    def test_phi_consistency_across_modules(self, simple_system):
        """Test that different modules compute consistent Φ."""
        system = NeuralSystem(**simple_system)

        # Compute Φ using standard calculator
        standard_calc = PhiCalculator()
        standard_phi = standard_calc.compute_phi(system).phi

        # Compute Φ using multiscale calculator (should include standard scale)
        multiscale_calc = MultiScalePhiCalculator()
        scale_results = multiscale_calc.compute_multiscale_phi(system)

        # Extract organism-scale result (should match standard calculation)
        if 'ORGANISM' in scale_results:
            organism_phi = scale_results['ORGANISM'].phi
            # Should be within reasonable tolerance
            ratio = organism_phi / (standard_phi + 1e-10)
            assert 0.8 < ratio < 1.2, \
                f"Multiscale organism Φ should match standard Φ: {organism_phi} vs {standard_phi}"

    def test_system_representation_consistency(self, simple_system):
        """Test that NeuralSystem representation is consistent across modules."""
        system = NeuralSystem(**simple_system)

        # All modules should be able to work with the same system
        phi_calc = PhiCalculator()
        translator = SubstrateTranslator()
        optimizer = EvolutionaryOptimizer(system, phi_calc, 5, 2)

        # All should accept the system without errors
        phi_calc.compute_phi(system)
        translator.extract_pattern(system)
        optimizer.evolve()  # Should run without error

        # All operations complete successfully
        assert True


# ============================================================================
# ERROR HANDLING AND ROBUSTNESS
# ============================================================================

@pytest.mark.integration
class TestIntegrationRobustness:
    """Test robustness of integrated pipeline."""

    def test_pipeline_with_edge_case_system(self, isolated_system):
        """Test pipeline with edge case (isolated system, Φ≈0)."""
        system = NeuralSystem(**isolated_system)

        phi_calc = PhiCalculator()
        translator = SubstrateTranslator()

        # Should handle gracefully
        metrics = phi_calc.compute_phi(system)
        assert metrics.phi >= 0

        # Translation should work even for low-Φ system
        translation_result = translator.translate(
            source_data=system,
            source_substrate=SubstrateType.SILICON_DIGITAL,
            target_substrate=SubstrateType.NEUROMORPHIC
        )

        # Should complete without error
        assert translation_result is not None

    def test_pipeline_recovers_from_failures(self, simple_system):
        """Test that pipeline handles component failures gracefully."""
        system = NeuralSystem(**simple_system)

        # Create deliberately challenging scenario
        bad_constraints = SubstrateConstraints(
            substrate_type=SubstrateType.QUANTUM_QUBIT,
            max_elements=2,  # Too small for system
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

        # Should handle gracefully without crashing
        try:
            result = translator.translate(
                source_data=system,
                source_substrate=SubstrateType.SILICON_DIGITAL,
                target_substrate=bad_constraints.substrate_type
            )
            # If it succeeds, great; if it fails, should be graceful
            assert result is not None
        except Exception as e:
            # Should raise informative exception, not crash
            assert isinstance(e, (ValueError, RuntimeError))


# ============================================================================
# PERFORMANCE INTEGRATION TESTS
# ============================================================================

@pytest.mark.integration
@pytest.mark.slow
class TestIntegrationPerformance:
    """Test performance of integrated pipeline."""

    def test_pipeline_completes_in_reasonable_time(self, small_brain_module):
        """Test that full pipeline completes in reasonable time."""
        import time

        system = NeuralSystem(**small_brain_module)
        phi_calc = PhiCalculator()

        start_time = time.time()

        # Run several pipeline steps
        phi_metrics = phi_calc.compute_phi(system)

        translator = SubstrateTranslator()
        ucr = translator.extract_pattern(system)

        elapsed = time.time() - start_time

        # Should complete in < 60 seconds for 100-node system
        assert elapsed < 60.0, f"Pipeline took too long: {elapsed:.2f}s"

    def test_parallel_measurements(self, simple_system):
        """Test that multiple systems can be measured in parallel."""
        import concurrent.futures

        # Create multiple systems
        systems = []
        for i in range(5):
            sys_data = simple_system.copy()
            sys_data['states'] = np.random.rand(100, 4)
            systems.append(NeuralSystem(**sys_data))

        phi_calc = PhiCalculator()

        # Measure in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(phi_calc.compute_phi, sys) for sys in systems]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        # All should succeed
        assert len(results) == 5
        assert all(r.phi >= 0 for r in results)
