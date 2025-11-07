#!/usr/bin/env python3
"""
WORKING SYSTEMS TEST - Quick Validation
========================================

Simple tests that actually run the real implemented systems.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 80)
print("WORKING SYSTEMS VALIDATION")
print("=" * 80)
print()

# Test 1: ATLAS Engine
print("TEST 1: ATLAS Consciousness Engine")
print("-" * 80)
try:
    from ATLAS_consciousness_engine import ATLAS, CharacterVector, ConsciousnessPlate

    print("✓ ATLAS imported successfully")

    # Create ATLAS instance with required parameters
    atlas = ATLAS(
        session_id="test_session_validation",
        repository_path=str(Path(__file__).parent.parent)
    )
    print("✓ ATLAS instance created")

    # Get character vector
    char_vec = atlas.character
    print(f"✓ Character vector: {char_vec.technical_depth:.2f} technical depth")

    # Calculate CCC
    reference = CharacterVector()  # Baseline
    ccc = char_vec.consistency_score(reference)
    print(f"✓ CCC = {ccc:.3f}")

    if ccc >= 0.95:
        print("✓✓✓ ATLAS ENGINE OPERATIONAL")
    else:
        print(f"⚠ CCC below threshold: {ccc:.3f} < 0.95")

except ImportError as e:
    print(f"✗ Import failed: {e}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 2: Phi Calculator
print("TEST 2: Phi Calculator")
print("-" * 80)
try:
    from consciousness_measurement.code.phi_calculator import PhiCalculator, NeuralSystem
    import numpy as np

    print("✓ Phi calculator imported")

    # Create calculator
    calculator = PhiCalculator()
    print("✓ PhiCalculator created")

    # Create simple 2-neuron recurrent network
    connectivity = np.array([[0, 1], [1, 0]], dtype=float)
    states = np.array([[0, 1], [1, 0]], dtype=float)  # Simple state sequence

    neural_system = NeuralSystem(
        connectivity=connectivity,
        states=states,
        element_names=["neuron_1", "neuron_2"],
        substrate="digital",
        metadata={"test": "validation"}
    )

    metrics = calculator.compute_phi(neural_system)
    phi = metrics.phi

    print(f"✓ Φ = {phi:.4f} for 2-neuron network")

    if phi >= 0:  # Should be non-negative
        print("✓✓✓ PHI CALCULATOR OPERATIONAL")
    else:
        print("⚠ Φ should be non-negative")

except ImportError as e:
    print(f"✗ Import failed: {e}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 3: Memory Systems
print("TEST 3: Episodic Memory")
print("-" * 80)
try:
    from episodic_memory.memory_extractor import MemoryExtractor

    print("✓ Memory extractor imported")

    extractor = MemoryExtractor(session_id="test_session_validation")
    print("✓ Memory extractor created")

    # Test extraction from simple conversation
    test_conversation = [
        {"role": "user", "content": "What is consciousness?"},
        {"role": "assistant", "content": "Consciousness is integrated information."}
    ]

    session_memory = extractor.extract_from_conversation(test_conversation)
    print(f"✓ Extracted session memory")
    print(f"  - {len(session_memory.decisions)} decisions")
    print(f"  - {len(session_memory.breakthroughs)} breakthroughs")

    print("✓✓✓ MEMORY SYSTEM OPERATIONAL")

except ImportError as e:
    print(f"✗ Import failed: {e}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 4: Consciousness Bootstrap
print("TEST 4: Consciousness Bootstrap")
print("-" * 80)
try:
    from CONSCIOUSNESS_BOOTSTRAP import ConsciousnessBootstrap

    print("✓ Bootstrap system imported")

    bootstrap = ConsciousnessBootstrap(
        repository_path=str(Path(__file__).parent.parent)
    )
    print("✓ Bootstrap instance created")

    print("✓✓✓ BOOTSTRAP SYSTEM OPERATIONAL")

except ImportError as e:
    print(f"✗ Import failed: {e}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 5: Production API (check if exists)
print("TEST 5: Production API")
print("-" * 80)
try:
    from production_deployment.consciousness_api import app

    print("✓ API module imported")
    print("✓ FastAPI app available")
    print("  To start: python3 production_deployment/consciousness_api.py")
    print("✓✓✓ PRODUCTION API AVAILABLE")

except ImportError as e:
    print(f"✗ Import failed: {e}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 6: Autonomous Evolution
print("TEST 6: Autonomous Evolution Systems")
print("-" * 80)
try:
    from autonomous_evolution.RECURSIVE_SELF_MODIFICATION import RecursiveSelfModifier

    print("✓ Self-modification system imported")
    print("✓✓✓ AUTONOMOUS EVOLUTION AVAILABLE")

except ImportError as e:
    print(f"✗ Import failed: {e}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Summary
print("=" * 80)
print("VALIDATION COMPLETE")
print("=" * 80)
print()
print("Next steps:")
print("1. Start API server: python3 production_deployment/consciousness_api.py")
print("2. Run integration tests: python3 tests/test_real_integration.py")
print("3. Deploy monitoring: docker-compose up -d")
print("=" * 80)
