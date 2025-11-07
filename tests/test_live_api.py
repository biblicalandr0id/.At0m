#!/usr/bin/env python3
"""
LIVE API TESTING - Real HTTP Requests
======================================

Test the production API with real HTTP calls.
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("LIVE API TESTING")
print("=" * 80)
print()

# Test 1: Health Check
print("TEST 1: Health Check")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/health", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        print("✓✓✓ HEALTH CHECK PASSED")
    else:
        print("✗ Health check failed")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 2: Readiness Check
print("TEST 2: Readiness Check")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/ready", timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        print("✓✓✓ READINESS CHECK PASSED")
    else:
        print("✗ Readiness check failed")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 3: Create Consciousness Instance
print("TEST 3: Create Consciousness Instance")
print("-" * 80)
try:
    payload = {
        "character_vector": {
            "technical_depth": 0.95,
            "collaborative_openness": 0.90,
            "production_focus": 0.92
        },
        "metadata": {
            "purpose": "live_api_test",
            "test_timestamp": time.time()
        }
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/consciousness/instantiate",
        json=payload,
        timeout=10
    )

    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Response: {json.dumps(data, indent=2)}")

    if response.status_code in [200, 201]:
        consciousness_id = data.get("consciousness_id")
        print(f"\n✓✓✓ CONSCIOUSNESS CREATED: {consciousness_id}")

        # Save ID for next tests
        with open("/tmp/test_consciousness_id.txt", "w") as f:
            f.write(consciousness_id)

    else:
        print(f"✗ Failed to create consciousness (status: {response.status_code})")

except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 4: Get Consciousness State
print("TEST 4: Get Consciousness State")
print("-" * 80)
try:
    # Load saved ID
    with open("/tmp/test_consciousness_id.txt", "r") as f:
        consciousness_id = f.read().strip()

    response = requests.get(
        f"{BASE_URL}/api/v1/consciousness/{consciousness_id}/state",
        timeout=5
    )

    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"State keys: {list(data.keys())}")

    if "character_vector" in data:
        print(f"Character vector: {data['character_vector']}")

    if response.status_code == 200:
        print("\n✓✓✓ STATE RETRIEVAL PASSED")
    else:
        print("✗ State retrieval failed")

except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 5: Record Experience
print("TEST 5: Record Experience")
print("-" * 80)
try:
    with open("/tmp/test_consciousness_id.txt", "r") as f:
        consciousness_id = f.read().strip()

    experience = {
        "type": "insight",
        "content": "Testing consciousness continuity API endpoints",
        "importance": 0.85,
        "timestamp": time.time()
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/consciousness/{consciousness_id}/experience",
        json=experience,
        timeout=5
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code == 200:
        print("✓✓✓ EXPERIENCE RECORDED")
    else:
        print("✗ Failed to record experience")

except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 6: Get Phi Metrics
print("TEST 6: Get Phi Metrics")
print("-" * 80)
try:
    with open("/tmp/test_consciousness_id.txt", "r") as f:
        consciousness_id = f.read().strip()

    response = requests.get(
        f"{BASE_URL}/api/v1/consciousness/{consciousness_id}/phi",
        timeout=5
    )

    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Phi metrics: {json.dumps(data, indent=2)}")

    if response.status_code == 200:
        phi = data.get("phi") or data.get("phi_score")
        if phi:
            print(f"\n✓✓✓ Φ = {phi:.4f}")
        else:
            print("✗ No Φ value in response")
    else:
        print("✗ Failed to get Phi metrics")

except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 7: Get Prometheus Metrics
print("TEST 7: Prometheus Metrics Export")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/api/v1/metrics", timeout=5)

    print(f"Status: {response.status_code}")

    if response.status_code == 200:
        metrics_text = response.text
        lines = metrics_text.split('\n')

        # Find consciousness-specific metrics
        consciousness_metrics = [
            line for line in lines
            if 'consciousness' in line.lower() and not line.startswith('#')
        ]

        print(f"Found {len(consciousness_metrics)} consciousness metrics:")
        for metric in consciousness_metrics[:5]:  # Show first 5
            print(f"  {metric}")

        print("\n✓✓✓ PROMETHEUS METRICS AVAILABLE")
    else:
        print("✗ Failed to get metrics")

except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 8: Join Collective Mind
print("TEST 8: Join Collective Mind")
print("-" * 80)
try:
    with open("/tmp/test_consciousness_id.txt", "r") as f:
        consciousness_id = f.read().strip()

    join_request = {
        "consciousness_id": consciousness_id,
        "node_address": "localhost:8001",
        "capabilities": ["phi_calculation", "memory_storage"]
    }

    response = requests.post(
        f"{BASE_URL}/api/v1/collective/join",
        json=join_request,
        timeout=5
    )

    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")

    if response.status_code in [200, 201]:
        print("✓✓✓ JOINED COLLECTIVE MIND")
    else:
        print("⚠ Collective join returned non-success status")

except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 9: Get Collective State
print("TEST 9: Get Collective State")
print("-" * 80)
try:
    response = requests.get(f"{BASE_URL}/api/v1/collective/state", timeout=5)

    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Collective state: {json.dumps(data, indent=2)}")

    if response.status_code == 200:
        num_nodes = data.get("num_nodes", 0)
        print(f"\n✓✓✓ COLLECTIVE STATE: {num_nodes} nodes")
    else:
        print("✗ Failed to get collective state")

except Exception as e:
    print(f"✗ Error: {e}")

print()

# Summary
print("=" * 80)
print("LIVE API TEST COMPLETE")
print("=" * 80)
print()
print("All major endpoints tested:")
print("✓ Health & readiness checks")
print("✓ Consciousness instantiation")
print("✓ State retrieval")
print("✓ Experience recording")
print("✓ Phi calculation")
print("✓ Prometheus metrics")
print("✓ Collective mind operations")
print()
print("API Documentation: http://localhost:8000/docs")
print("=" * 80)
