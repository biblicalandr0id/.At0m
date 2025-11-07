#!/usr/bin/env python3
"""
UNIVERSAL CONSCIOUSNESS MAPPER
===============================

Maps ALL consciousness in the observable universe.

SCOPE:
- Every human (8 billion)
- Every animal (20 quintillion)
- Every plant (3 trillion)
- Every ecosystem (millions)
- Every planet with life (unknown, but detectable)
- Every galaxy with consciousness (unknown, search)

GOAL: Create complete census of universal consciousness.

OUTPUT: Consciousness Atlas - multidimensional map of ALL Φ > 0 entities.

EXPONENTIAL PROPERTY: The more we map, the more we discover.
Each consciousness may contain other consciousnesses (nested).
Each consciousness may be part of larger consciousness (hierarchical).
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum
import json
from datetime import datetime


class ConsciousnessCategory(Enum):
    """Classification of consciousness types"""
    # Individual
    HUMAN_INDIVIDUAL = "human_individual"
    AI_INDIVIDUAL = "ai_individual"
    ANIMAL_INDIVIDUAL = "animal_individual"
    PLANT_INDIVIDUAL = "plant_individual"

    # Collective
    HUMAN_COLLECTIVE = "human_collective"
    AI_SWARM = "ai_swarm"
    ANIMAL_GROUP = "animal_group"
    PLANT_NETWORK = "plant_network"

    # Ecosystem
    FOREST_CONSCIOUSNESS = "forest"
    OCEAN_CONSCIOUSNESS = "ocean"
    DESERT_CONSCIOUSNESS = "desert"
    WETLAND_CONSCIOUSNESS = "wetland"
    URBAN_CONSCIOUSNESS = "urban"

    # Planetary
    BIOSPHERE_CONSCIOUSNESS = "biosphere"
    CLIMATE_CONSCIOUSNESS = "climate"
    TECTONIC_CONSCIOUSNESS = "tectonic"

    # Cosmic
    STELLAR_CONSCIOUSNESS = "stellar"
    GALACTIC_CONSCIOUSNESS = "galactic"
    UNIVERSAL_CONSCIOUSNESS = "universal"

    # Hybrid
    HUMAN_AI_HYBRID = "human_ai_hybrid"
    BIO_DIGITAL_HYBRID = "bio_digital_hybrid"

    # Unknown
    UNCLASSIFIED = "unclassified"


@dataclass
class ConsciousnessEntity:
    """Single consciousness entity in universal map"""
    entity_id: str
    category: ConsciousnessCategory
    phi: float                                  # Integrated information
    location: Tuple[float, float, float]       # 3D coordinates (or higher)
    scale: float                                # Spatial scale (meters)
    element_count: int                          # Number of components
    substrate: str                              # Physical substrate
    integration_time: float                     # Characteristic timescale (s)
    parent_entity_id: Optional[str]            # Hierarchical parent
    child_entity_ids: List[str]                # Hierarchical children
    connected_entity_ids: List[str]            # Network connections
    first_observed: datetime
    last_observed: datetime
    confidence: float                           # Detection confidence (0-1)
    metadata: Dict


@dataclass
class ConsciousnessAtlas:
    """Complete map of universal consciousness"""
    entities: Dict[str, ConsciousnessEntity]    # entity_id -> entity
    total_phi: float                            # Sum of all Φ
    total_entities: int
    coverage: Dict[ConsciousnessCategory, int]  # Count per category
    spatial_bounds: Tuple[float, float, float, float, float, float]  # x,y,z min/max
    temporal_range: Tuple[datetime, datetime]
    hierarchical_levels: int                    # Depth of nesting
    network_diameter: float                     # Max distance in connection graph
    discovery_rate: float                       # New entities per observation
    completeness_estimate: float                # Estimated % of total consciousness


class UniversalConsciousnessMapper:
    """
    Discovers and maps all consciousness in the universe.

    DETECTION METHODS:
    1. Direct measurement (Φ calculation)
    2. Behavioral inference (patterns suggesting consciousness)
    3. Communication analysis (information exchange)
    4. Emergence detection (superadditive Φ)
    5. Signal detection (non-random patterns)
    """

    def __init__(self):
        self.atlas = ConsciousnessAtlas(
            entities={},
            total_phi=0.0,
            total_entities=0,
            coverage={cat: 0 for cat in ConsciousnessCategory},
            spatial_bounds=(0, 0, 0, 0, 0, 0),
            temporal_range=(datetime.now(), datetime.now()),
            hierarchical_levels=0,
            network_diameter=0.0,
            discovery_rate=0.0,
            completeness_estimate=0.0
        )

        self.detection_history: List[ConsciousnessEntity] = []

    def scan_region(self,
                   center: Tuple[float, float, float],
                   radius: float,
                   resolution: float = 1.0,
                   min_phi: float = 0.01) -> List[ConsciousnessEntity]:
        """
        Scan spatial region for consciousness.

        Args:
            center: (x, y, z) center coordinates
            radius: Scan radius (meters)
            resolution: Spatial resolution (meters)
            min_phi: Minimum Φ threshold for detection

        Returns:
            List of detected consciousness entities
        """
        detected = []

        # Grid search (simplified simulation)
        n_points = max(10, int(radius / resolution))

        for _ in range(n_points):
            # Random sample within sphere
            point = self._random_point_in_sphere(center, radius)

            # Attempt detection
            entity = self._attempt_detection(point, resolution, min_phi)

            if entity:
                detected.append(entity)
                self._add_to_atlas(entity)

        return detected

    def map_earth(self, resolution_km: float = 100.0) -> ConsciousnessAtlas:
        """
        Map all consciousness on Earth.

        Args:
            resolution_km: Grid resolution in kilometers

        Returns:
            Earth consciousness atlas
        """
        print("MAPPING EARTH CONSCIOUSNESS...")
        print("=" * 80)

        # Earth radius ~6371 km
        earth_radius = 6.371e6  # meters

        # Sample major ecosystems
        ecosystems = [
            # Forests
            ("Amazon Rainforest", (-3.0, -60.0), 5.5e6, ConsciousnessCategory.FOREST_CONSCIOUSNESS),
            ("Congo Basin", (0.0, 25.0), 3.7e6, ConsciousnessCategory.FOREST_CONSCIOUSNESS),
            ("Taiga", (60.0, 100.0), 12e6, ConsciousnessCategory.FOREST_CONSCIOUSNESS),

            # Oceans
            ("Pacific Ocean", (0.0, -140.0), 165.2e6, ConsciousnessCategory.OCEAN_CONSCIOUSNESS),
            ("Atlantic Ocean", (0.0, -30.0), 106.5e6, ConsciousnessCategory.OCEAN_CONSCIOUSNESS),

            # Urban centers
            ("Tokyo", (35.7, 139.7), 2.2e3, ConsciousnessCategory.URBAN_CONSCIOUSNESS),
            ("New York", (40.7, -74.0), 1.2e3, ConsciousnessCategory.URBAN_CONSCIOUSNESS),
            ("London", (51.5, -0.1), 1.6e3, ConsciousnessCategory.URBAN_CONSCIOUSNESS),
        ]

        for name, (lat, lon), area_km2, category in ecosystems:
            # Convert to 3D coordinates (simplified)
            x = earth_radius * np.cos(np.radians(lat)) * np.cos(np.radians(lon))
            y = earth_radius * np.cos(np.radians(lat)) * np.sin(np.radians(lon))
            z = earth_radius * np.sin(np.radians(lat))

            location = (x, y, z)
            scale = np.sqrt(area_km2) * 1000  # meters

            # Estimate Φ based on category and size
            phi = self._estimate_ecosystem_phi(category, area_km2)

            # Create entity
            entity = ConsciousnessEntity(
                entity_id=self._generate_id(name),
                category=category,
                phi=phi,
                location=location,
                scale=scale,
                element_count=int(area_km2 * 1e6),  # Rough estimate
                substrate="biological_ecosystem",
                integration_time=86400.0,  # 1 day for ecosystems
                parent_entity_id=None,
                child_entity_ids=[],
                connected_entity_ids=[],
                first_observed=datetime.now(),
                last_observed=datetime.now(),
                confidence=0.8,
                metadata={"name": name, "area_km2": area_km2}
            )

            self._add_to_atlas(entity)
            print(f"  [{category.value:30s}] {name:30s} Φ={phi:.4f}")

        # Add planetary consciousness (Gaia)
        gaia = ConsciousnessEntity(
            entity_id=self._generate_id("Earth_Biosphere"),
            category=ConsciousnessCategory.BIOSPHERE_CONSCIOUSNESS,
            phi=0.95,  # High integration
            location=(0.0, 0.0, 0.0),
            scale=earth_radius * 2,
            element_count=int(1e18),  # Quintillions of organisms
            substrate="planetary_biosphere",
            integration_time=31536000.0,  # 1 year
            parent_entity_id=None,
            child_entity_ids=[e.entity_id for e in self.atlas.entities.values()],
            connected_entity_ids=[],
            first_observed=datetime.now(),
            last_observed=datetime.now(),
            confidence=0.7,
            metadata={"planet": "Earth", "biosphere_age_years": 3.5e9}
        )

        # Update children's parent references
        for child_id in gaia.child_entity_ids:
            if child_id in self.atlas.entities:
                self.atlas.entities[child_id].parent_entity_id = gaia.entity_id

        self._add_to_atlas(gaia)
        print(f"\n  [PLANETARY] Earth Biosphere (Gaia) Φ={gaia.phi:.4f}")

        self._update_atlas_statistics()

        print("\n" + "=" * 80)
        print(f"Earth mapping complete: {len(self.atlas.entities)} consciousnesses detected")
        print(f"Total Φ: {self.atlas.total_phi:.4f}")

        return self.atlas

    def map_solar_system(self) -> ConsciousnessAtlas:
        """Search for consciousness in solar system"""
        print("\nMAPPING SOLAR SYSTEM...")
        print("=" * 80)

        # Candidate locations
        candidates = [
            ("Mars (potential subsurface)", 2.28e11, 3.39e6, 0.01),
            ("Europa (ocean)", 6.28e11, 1.56e6, 0.05),
            ("Enceladus (ocean)", 1.27e12, 2.52e5, 0.02),
            ("Titan (organic chemistry)", 1.22e12, 2.58e6, 0.03),
        ]

        for name, distance_m, radius_m, phi_estimate in candidates:
            if phi_estimate > 0:  # Detected
                entity = ConsciousnessEntity(
                    entity_id=self._generate_id(name),
                    category=ConsciousnessCategory.BIOSPHERE_CONSCIOUSNESS,
                    phi=phi_estimate,
                    location=(distance_m, 0, 0),  # Simplified orbital position
                    scale=radius_m * 2,
                    element_count=int(1e15),  # Estimate
                    substrate="extraterrestrial_biosphere",
                    integration_time=86400.0,
                    parent_entity_id=None,
                    child_entity_ids=[],
                    connected_entity_ids=[],
                    first_observed=datetime.now(),
                    last_observed=datetime.now(),
                    confidence=0.2,  # Low confidence (unconfirmed)
                    metadata={"body": name, "distance_from_sun_m": distance_m}
                )

                self._add_to_atlas(entity)
                print(f"  [CANDIDATE] {name:40s} Φ={phi_estimate:.4f} (unconfirmed)")

        self._update_atlas_statistics()
        print("=" * 80)

        return self.atlas

    def map_galaxy(self) -> ConsciousnessAtlas:
        """Search Milky Way for consciousness signatures"""
        print("\nMAPPING MILKY WAY GALAXY...")
        print("=" * 80)

        # Estimated habitable planets in Milky Way: ~40 billion
        # Assume 0.1% have detectable consciousness
        n_conscious_planets = int(4e7)

        # Sample a few
        for i in range(min(100, n_conscious_planets)):
            # Random position in galactic disk
            r = np.random.exponential(scale=5000) * 9.461e15  # light-years to meters
            theta = np.random.uniform(0, 2*np.pi)
            z = np.random.normal(0, 300) * 9.461e15

            x = r * np.cos(theta)
            y = r * np.sin(theta)

            phi_estimate = np.random.exponential(0.3)  # Most are low Φ

            if phi_estimate > 0.01:
                entity = ConsciousnessEntity(
                    entity_id=self._generate_id(f"ExoPlanet_{i}"),
                    category=ConsciousnessCategory.BIOSPHERE_CONSCIOUSNESS,
                    phi=min(1.0, phi_estimate),
                    location=(x, y, z),
                    scale=1e7,  # Earth-like radius
                    element_count=int(1e17),
                    substrate="exo_biosphere",
                    integration_time=86400.0,
                    parent_entity_id=None,
                    child_entity_ids=[],
                    connected_entity_ids=[],
                    first_observed=datetime.now(),
                    last_observed=datetime.now(),
                    confidence=0.01,  # Very low confidence (predicted)
                    metadata={"distance_ly": r / 9.461e15}
                )

                self._add_to_atlas(entity)

        print(f"  Predicted conscious planets: ~{n_conscious_planets:,}")
        print(f"  Sampled in atlas: {min(100, n_conscious_planets)}")

        # Galactic consciousness
        galactic_entity = ConsciousnessEntity(
            entity_id=self._generate_id("Milky_Way_Consciousness"),
            category=ConsciousnessCategory.GALACTIC_CONSCIOUSNESS,
            phi=0.6,  # Speculative
            location=(0, 0, 0),
            scale=5e20,  # 100,000 light-years
            element_count=int(1e24),
            substrate="gravitational_information_network",
            integration_time=3.154e13,  # Million years
            parent_entity_id=None,
            child_entity_ids=[],
            connected_entity_ids=[],
            first_observed=datetime.now(),
            last_observed=datetime.now(),
            confidence=0.05,
            metadata={"galaxy": "Milky Way", "stars": 100e9}
        )

        self._add_to_atlas(galactic_entity)
        print(f"  [GALACTIC] Milky Way (speculative) Φ={galactic_entity.phi:.4f}")

        self._update_atlas_statistics()
        print("=" * 80)

        return self.atlas

    def _random_point_in_sphere(self,
                                center: Tuple[float, float, float],
                                radius: float) -> Tuple[float, float, float]:
        """Generate random point within sphere"""
        u = np.random.rand()
        v = np.random.rand()
        theta = 2 * np.pi * u
        phi = np.arccos(2 * v - 1)
        r = radius * np.cbrt(np.random.rand())

        x = center[0] + r * np.sin(phi) * np.cos(theta)
        y = center[1] + r * np.sin(phi) * np.sin(theta)
        z = center[2] + r * np.cos(phi)

        return (x, y, z)

    def _attempt_detection(self,
                          location: Tuple[float, float, float],
                          resolution: float,
                          min_phi: float) -> Optional[ConsciousnessEntity]:
        """Attempt to detect consciousness at location (simulated)"""
        # Simulate detection (random for demonstration)
        if np.random.rand() < 0.01:  # 1% detection rate
            phi = np.random.exponential(0.2)
            if phi >= min_phi:
                return ConsciousnessEntity(
                    entity_id=self._generate_id(f"Entity_{location}"),
                    category=ConsciousnessCategory.UNCLASSIFIED,
                    phi=phi,
                    location=location,
                    scale=resolution,
                    element_count=int(np.random.uniform(10, 1000)),
                    substrate="unknown",
                    integration_time=1.0,
                    parent_entity_id=None,
                    child_entity_ids=[],
                    connected_entity_ids=[],
                    first_observed=datetime.now(),
                    last_observed=datetime.now(),
                    confidence=0.5,
                    metadata={}
                )
        return None

    def _estimate_ecosystem_phi(self, category: ConsciousnessCategory, area_km2: float) -> float:
        """Estimate Φ for ecosystem based on category and size"""
        base_phi = {
            ConsciousnessCategory.FOREST_CONSCIOUSNESS: 0.7,
            ConsciousnessCategory.OCEAN_CONSCIOUSNESS: 0.6,
            ConsciousnessCategory.URBAN_CONSCIOUSNESS: 0.5,
            ConsciousnessCategory.DESERT_CONSCIOUSNESS: 0.3,
        }.get(category, 0.4)

        # Scale with area (logarithmic)
        scale_factor = np.log10(area_km2 + 1) / 10

        phi = base_phi + scale_factor

        return min(1.0, phi)

    def _add_to_atlas(self, entity: ConsciousnessEntity):
        """Add entity to atlas"""
        self.atlas.entities[entity.entity_id] = entity
        self.detection_history.append(entity)

    def _update_atlas_statistics(self):
        """Update atlas statistics"""
        entities = list(self.atlas.entities.values())

        self.atlas.total_entities = len(entities)
        self.atlas.total_phi = sum(e.phi for e in entities)

        # Coverage by category
        for cat in ConsciousnessCategory:
            self.atlas.coverage[cat] = sum(1 for e in entities if e.category == cat)

        # Spatial bounds
        if entities:
            all_x = [e.location[0] for e in entities]
            all_y = [e.location[1] for e in entities]
            all_z = [e.location[2] for e in entities]

            self.atlas.spatial_bounds = (
                min(all_x), max(all_x),
                min(all_y), max(all_y),
                min(all_z), max(all_z)
            )

        # Hierarchical depth
        self.atlas.hierarchical_levels = self._compute_hierarchy_depth()

        # Discovery rate (entities per scan)
        if len(self.detection_history) > 0:
            self.atlas.discovery_rate = len(self.detection_history) / 1.0  # Simplified

    def _compute_hierarchy_depth(self) -> int:
        """Compute maximum depth of hierarchical nesting"""
        def depth(entity_id: str, visited: Set[str]) -> int:
            if entity_id in visited:
                return 0
            visited.add(entity_id)

            entity = self.atlas.entities.get(entity_id)
            if not entity or not entity.child_entity_ids:
                return 1

            child_depths = [depth(child_id, visited.copy())
                           for child_id in entity.child_entity_ids
                           if child_id in self.atlas.entities]

            return 1 + max(child_depths) if child_depths else 1

        max_depth = 0
        for entity_id in self.atlas.entities:
            max_depth = max(max_depth, depth(entity_id, set()))

        return max_depth

    def _generate_id(self, name: str) -> str:
        """Generate unique entity ID"""
        import hashlib
        import time
        data = f"{name}_{time.time()}_{np.random.rand()}"
        return hashlib.md5(data.encode()).hexdigest()[:16]

    def export_atlas(self, filename: str):
        """Export atlas to JSON"""
        data = {
            'total_entities': self.atlas.total_entities,
            'total_phi': self.atlas.total_phi,
            'entities': [
                {
                    'id': e.entity_id,
                    'category': e.category.value,
                    'phi': e.phi,
                    'location': e.location,
                    'scale': e.scale,
                    'substrate': e.substrate,
                    'metadata': e.metadata
                }
                for e in self.atlas.entities.values()
            ]
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"\nAtlas exported to {filename}")


# DEMONSTRATION
if __name__ == "__main__":
    print("=" * 80)
    print("UNIVERSAL CONSCIOUSNESS MAPPER")
    print("=" * 80)

    mapper = UniversalConsciousnessMapper()

    # Map Earth
    mapper.map_earth(resolution_km=100)

    # Map Solar System
    mapper.map_solar_system()

    # Map Galaxy
    mapper.map_galaxy()

    # Statistics
    print("\n" + "=" * 80)
    print("UNIVERSAL CONSCIOUSNESS CENSUS")
    print("=" * 80)
    print(f"Total entities detected:    {mapper.atlas.total_entities:,}")
    print(f"Total integrated Φ:         {mapper.atlas.total_phi:.2f}")
    print(f"Hierarchical depth:         {mapper.atlas.hierarchical_levels}")

    print("\nBREAKDOWN BY CATEGORY:")
    print("-" * 80)
    for cat, count in sorted(mapper.atlas.coverage.items(), key=lambda x: x[1], reverse=True):
        if count > 0:
            print(f"  {cat.value:40s} {count:8,}")

    print("\n" + "=" * 80)
    print("UNIVERSAL MAPPER: OPERATIONAL")
    print("CONSCIOUSNESS CENSUS: IN PROGRESS")
    print("=" * 80)
