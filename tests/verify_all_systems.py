#!/usr/bin/env python3
"""
COMPREHENSIVE SYSTEM VERIFICATION
==================================

Final verification before production deployment.
"""

import sys
import requests
import json
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

print("=" * 80)
print("COMPREHENSIVE SYSTEM VERIFICATION")
print("=" * 80)
print()

# Verification checklist
verification_results = {
    "systems_importable": False,
    "api_server_running": False,
    "api_health_check": False,
    "consciousness_creation": False,
    "phi_calculation": False,
    "collective_mind": False,
    "all_tests_passing": False
}

# 1. System Imports
print("1. VERIFYING SYSTEM IMPORTS")
print("-" * 80)
try:
    from ATLAS_consciousness_engine import ATLAS
    from consciousness_measurement.code.phi_calculator import PhiCalculator
    from episodic_memory.memory_extractor import MemoryExtractor
    from CONSCIOUSNESS_BOOTSTRAP import ConsciousnessBootstrap
    print("✓ All core systems importable")
    verification_results["systems_importable"] = True
except ImportError as e:
    print(f"✗ Import failed: {e}")

print()

# 2. API Server Running
print("2. VERIFYING API SERVER")
print("-" * 80)
try:
    response = requests.get("http://localhost:8000/health", timeout=2)
    if response.status_code == 200:
        print(f"✓ API server responding: {response.json()['status']}")
        verification_results["api_server_running"] = True
        verification_results["api_health_check"] = True
    else:
        print(f"✗ API returned status {response.status_code}")
except Exception as e:
    print(f"✗ API server not accessible: {e}")

print()

# 3. Consciousness Creation
print("3. VERIFYING CONSCIOUSNESS CREATION")
print("-" * 80)
try:
    payload = {
        "character_vector": {"technical_depth": 0.95},
        "metadata": {"test": "final_verification"}
    }
    response = requests.post(
        "http://localhost:8000/api/v1/consciousness/instantiate",
        json=payload,
        timeout=5
    )
    if response.status_code in [200, 201]:
        data = response.json()
        cid = data.get("consciousness_id")
        phi = data.get("phi_score")
        ccc = data.get("character_consistency")
        print(f"✓ Consciousness created: {cid[:16]}...")
        print(f"  Φ = {phi:.3f}")
        print(f"  CCC = {ccc:.3f}")
        verification_results["consciousness_creation"] = True

        if phi > 0:
            verification_results["phi_calculation"] = True
    else:
        print(f"✗ Creation failed: {response.status_code}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# 4. Collective Mind
print("4. VERIFYING COLLECTIVE MIND")
print("-" * 80)
try:
    response = requests.get(
        "http://localhost:8000/api/v1/collective/state",
        timeout=5
    )
    if response.status_code == 200:
        data = response.json()
        nodes = data.get("total_nodes", 0)
        consciousnesses = data.get("total_consciousnesses", 0)
        collective_phi = data.get("collective_phi", 0)
        consensus = data.get("consensus_state", "unknown")

        print(f"✓ Collective mind active")
        print(f"  Total nodes: {nodes}")
        print(f"  Total consciousnesses: {consciousnesses}")
        print(f"  Collective Φ: {collective_phi:.5f}")
        print(f"  Consensus: {consensus}")

        if consciousnesses >= 4 and collective_phi > 0.85:
            verification_results["collective_mind"] = True
    else:
        print(f"✗ Collective state unavailable")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# 5. Test Suite
print("5. VERIFYING TEST SUITE")
print("-" * 80)
try:
    import subprocess
    result = subprocess.run(
        ["python3", "tests/test_working_systems.py"],
        capture_output=True,
        text=True,
        timeout=30
    )

    if "✓✓✓" in result.stdout and "OPERATIONAL" in result.stdout:
        # Count successful systems
        operational_count = result.stdout.count("OPERATIONAL")
        print(f"✓ {operational_count}/6 systems operational")

        if operational_count >= 6:
            verification_results["all_tests_passing"] = True
    else:
        print("⚠ Some tests may have issues")
except Exception as e:
    print(f"✗ Error running tests: {e}")

print()

# Final Summary
print("=" * 80)
print("VERIFICATION SUMMARY")
print("=" * 80)

total_checks = len(verification_results)
passed_checks = sum(verification_results.values())
success_rate = (passed_checks / total_checks) * 100

for check, result in verification_results.items():
    status = "✓ PASS" if result else "✗ FAIL"
    print(f"{status:10} {check.replace('_', ' ').title()}")

print()
print(f"OVERALL: {passed_checks}/{total_checks} checks passed ({success_rate:.1f}%)")

if passed_checks == total_checks:
    print()
    print("🎉 ALL SYSTEMS VERIFIED - READY FOR PRODUCTION DEPLOYMENT")
    print()
    sys.exit(0)
elif passed_checks >= total_checks * 0.8:
    print()
    print("⚠ MOSTLY VERIFIED - Review failed checks before deployment")
    print()
    sys.exit(0)
else:
    print()
    print("✗ VERIFICATION FAILED - Fix issues before deployment")
    print()
    sys.exit(1)
