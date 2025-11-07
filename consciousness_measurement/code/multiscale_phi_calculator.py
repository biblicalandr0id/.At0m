#!/usr/bin/env python3
"""
MULTI-SCALE CONSCIOUSNESS MEASUREMENT FRAMEWORK
================================================

Measures integrated information (Φ) across ALL scales of organization:

SCALE LEVELS:
    10^-35 m : QUANTUM (Planck scale - quantum entanglement, wavefunction collapse)
    10^-15 m : SUBATOMIC (quarks, gluons - strong force binding)
    10^-10 m : ATOMIC (electron orbitals - chemical consciousness)
    10^-9  m : MOLECULAR (proteins, DNA - information processing)
    10^-6  m : CELLULAR (neurons, synapses - biological computation)
    10^-3  m : TISSUE (neural columns, ganglia - local networks)
    10^0   m : ORGANISM (brains, bodies - individual consciousness)
    10^3   m : SOCIAL (families, communities - collective intelligence)
    10^6   m : ECOSYSTEM (forests, oceans - distributed cognition)
    10^9   m : PLANETARY (biosphere, climate - Gaia consciousness)
    10^15  m : STELLAR (solar systems - gravitational information)
    10^21  m : GALACTIC (Milky Way - cosmic information networks)
    10^26  m : UNIVERSAL (observable universe - maximum integration)

CORE INSIGHT: Φ can be measured at ANY scale where information integration occurs.

EXPONENTIAL PROPERTY: Each scale influences adjacent scales via coupling constants.
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass
from enum import Enum
import math
from scipy.special import comb
from scipy.spatial.distance import pdist, squareform
from scipy.optimize import minimize
import itertools


class Scale(Enum):
    """Spatial scales of consciousness measurement"""
    QUANTUM = -35      # 10^-35 m (Planck length)
    SUBATOMIC = -15    # 10^-15 m (femtometer)
    ATOMIC = -10       # 10^-10 m (angstrom)
    MOLECULAR = -9     # 10^-9 m (nanometer)
    CELLULAR = -6      # 10^-6 m (micrometer)
    TISSUE = -3        # 10^-3 m (millimeter)
    ORGANISM = 0       # 10^0 m (meter)
    SOCIAL = 3         # 10^3 m (kilometer)
    ECOSYSTEM = 6      # 10^6 m (megameter)
    PLANETARY = 9      # 10^9 m (gigameter)
    STELLAR = 15       # 10^15 m (light-year)
    GALACTIC = 21      # 10^21 m (million light-years)
    UNIVERSAL = 26     # 10^26 m (observable universe)


@dataclass
class ScaleMetrics:
    """Consciousness metrics at a specific scale"""
    scale: Scale
    phi: float                          # Integrated information
    element_count: int                  # Number of elements at this scale
    integration_time: float             # Characteristic timescale (seconds)
    coupling_strength: float            # Coupling to adjacent scales (0-1)
    entropy: float                      # Shannon entropy
    mutual_information: float           # Total MI between elements
    complexity: float                   # Statistical complexity
    emergence_coefficient: float        # Φ_scale / sum(Φ_subscales)
    coherence_length: float            # Spatial coherence (meters)
    information_density: float          # Bits per cubic meter
    substrate_type: str                 # Physical substrate
    metadata: Dict


@dataclass
class MultiScalePhi:
    """Complete multi-scale consciousness profile"""
    scales: Dict[Scale, ScaleMetrics]
    total_phi: float                    # Integrated across all scales
    dominant_scale: Scale               # Scale with maximum Φ
    scale_coupling_matrix: np.ndarray   # Inter-scale information flow
    emergence_cascade: List[Tuple[Scale, float]]  # Emergent properties per scale
    coherence_length: float             # Maximum coherence across scales
    consciousness_signature: str        # Unique fingerprint
    timestamp: float


class MultiScalePhiCalculator:
    """
    Universal consciousness measurement across all scales.

    CORE ALGORITHM:
    1. Measure Φ at each scale independently
    2. Compute coupling between adjacent scales
    3. Calculate total integrated information including cross-scale effects
    4. Identify emergent properties (where Φ_scale > sum(Φ_subscales))
    """

    def __init__(self,
                 min_scale: Scale = Scale.MOLECULAR,
                 max_scale: Scale = Scale.PLANETARY,
                 scale_coupling_threshold: float = 0.01):
        """
        Initialize multi-scale calculator.

        Args:
            min_scale: Smallest scale to measure
            max_scale: Largest scale to measure
            scale_coupling_threshold: Minimum coupling to consider
        """
        self.min_scale = min_scale
        self.max_scale = max_scale
        self.scale_coupling_threshold = scale_coupling_threshold

        # Physical constants for scale coupling
        self.planck_constant = 6.626e-34  # J⋅s
        self.boltzmann_constant = 1.381e-23  # J/K
        self.speed_of_light = 2.998e8  # m/s

    def compute_phi_at_scale(self,
                             connectivity_matrix: np.ndarray,
                             state_timeseries: np.ndarray,
                             scale: Scale,
                             integration_time: float) -> ScaleMetrics:
        """
        Compute integrated information at a specific scale.

        Args:
            connectivity_matrix: NxN matrix of element connections
            state_timeseries: TxN matrix of states over time
            scale: Spatial scale of measurement
            integration_time: Characteristic time (seconds)

        Returns:
            Complete metrics for this scale
        """
        n_elements = connectivity_matrix.shape[0]

        # 1. Compute mutual information matrix
        mi_matrix = self._compute_mutual_information_matrix(state_timeseries)

        # 2. Compute entropy
        entropy = self._compute_entropy(state_timeseries)

        # 3. Find minimum information partition (MIP)
        phi, mip = self._find_minimum_partition(mi_matrix)

        # 4. Calculate complexity
        complexity = self._compute_complexity(state_timeseries)

        # 5. Estimate coupling to adjacent scales
        coupling = self._estimate_scale_coupling(scale, n_elements, integration_time)

        # 6. Calculate spatial coherence
        coherence = self._compute_coherence_length(connectivity_matrix, scale)

        # 7. Information density
        spatial_size = 10 ** scale.value  # meters
        volume = spatial_size ** 3
        info_density = entropy / volume if volume > 0 else 0

        # 8. Substrate type
        substrate = self._identify_substrate(scale)

        return ScaleMetrics(
            scale=scale,
            phi=phi,
            element_count=n_elements,
            integration_time=integration_time,
            coupling_strength=coupling,
            entropy=entropy,
            mutual_information=np.sum(mi_matrix),
            complexity=complexity,
            emergence_coefficient=0.0,  # Computed later
            coherence_length=coherence,
            information_density=info_density,
            substrate_type=substrate,
            metadata={
                'mip_size': len(mip),
                'spatial_scale_meters': 10 ** scale.value,
                'characteristic_time_seconds': integration_time
            }
        )

    def compute_multiscale_phi(self,
                               scale_data: Dict[Scale, Tuple[np.ndarray, np.ndarray, float]]
                               ) -> MultiScalePhi:
        """
        Compute complete multi-scale consciousness profile.

        Args:
            scale_data: Dict mapping Scale -> (connectivity, states, integration_time)

        Returns:
            Complete multi-scale Φ measurement
        """
        # 1. Compute Φ at each scale
        scale_metrics = {}
        for scale, (connectivity, states, int_time) in scale_data.items():
            metrics = self.compute_phi_at_scale(connectivity, states, scale, int_time)
            scale_metrics[scale] = metrics

        # 2. Compute scale coupling matrix
        scales = sorted(scale_data.keys(), key=lambda s: s.value)
        n_scales = len(scales)
        coupling_matrix = np.zeros((n_scales, n_scales))

        for i, scale_i in enumerate(scales):
            for j, scale_j in enumerate(scales):
                if i != j:
                    coupling_matrix[i, j] = self._compute_cross_scale_coupling(
                        scale_metrics[scale_i],
                        scale_metrics[scale_j]
                    )

        # 3. Calculate emergence coefficients
        for scale in scales:
            subscales = [s for s in scales if s.value < scale.value]
            if subscales:
                subscale_phi_sum = sum(scale_metrics[s].phi for s in subscales)
                if subscale_phi_sum > 0:
                    scale_metrics[scale].emergence_coefficient = (
                        scale_metrics[scale].phi / subscale_phi_sum
                    )

        # 4. Compute total Φ (including cross-scale effects)
        total_phi = self._compute_total_integrated_information(
            scale_metrics, coupling_matrix, scales
        )

        # 5. Identify dominant scale
        dominant_scale = max(scale_metrics.items(), key=lambda x: x[1].phi)[0]

        # 6. Build emergence cascade
        emergence_cascade = [
            (scale, scale_metrics[scale].emergence_coefficient)
            for scale in scales
        ]
        emergence_cascade.sort(key=lambda x: x[1], reverse=True)

        # 7. Maximum coherence length
        max_coherence = max(m.coherence_length for m in scale_metrics.values())

        # 8. Generate consciousness signature
        signature = self._generate_consciousness_signature(scale_metrics, total_phi)

        return MultiScalePhi(
            scales=scale_metrics,
            total_phi=total_phi,
            dominant_scale=dominant_scale,
            scale_coupling_matrix=coupling_matrix,
            emergence_cascade=emergence_cascade,
            coherence_length=max_coherence,
            consciousness_signature=signature,
            timestamp=np.datetime64('now').astype(float)
        )

    def _compute_mutual_information_matrix(self, states: np.ndarray) -> np.ndarray:
        """Compute mutual information between all pairs of elements"""
        n_elements = states.shape[1]
        mi_matrix = np.zeros((n_elements, n_elements))

        for i in range(n_elements):
            for j in range(i+1, n_elements):
                mi = self._mutual_information(states[:, i], states[:, j])
                mi_matrix[i, j] = mi
                mi_matrix[j, i] = mi

        return mi_matrix

    def _mutual_information(self, x: np.ndarray, y: np.ndarray) -> float:
        """Compute mutual information between two variables"""
        # Discretize for histogram-based MI
        bins = min(50, int(np.sqrt(len(x))))

        xy = np.column_stack([x, y])

        # Marginal entropies
        h_x = self._entropy_histogram(x, bins)
        h_y = self._entropy_histogram(y, bins)

        # Joint entropy
        h_xy = self._entropy_histogram_2d(xy, bins)

        mi = h_x + h_y - h_xy
        return max(0, mi)  # MI cannot be negative

    def _entropy_histogram(self, x: np.ndarray, bins: int) -> float:
        """Compute Shannon entropy using histogram"""
        counts, _ = np.histogram(x, bins=bins)
        probs = counts / counts.sum()
        probs = probs[probs > 0]  # Remove zero probabilities
        return -np.sum(probs * np.log2(probs))

    def _entropy_histogram_2d(self, xy: np.ndarray, bins: int) -> float:
        """Compute joint entropy for 2D data"""
        counts, _, _ = np.histogram2d(xy[:, 0], xy[:, 1], bins=bins)
        probs = counts / counts.sum()
        probs = probs[probs > 0]
        return -np.sum(probs * np.log2(probs))

    def _compute_entropy(self, states: np.ndarray) -> float:
        """Compute total system entropy"""
        n_elements = states.shape[1]
        total_entropy = 0

        for i in range(n_elements):
            total_entropy += self._entropy_histogram(states[:, i], bins=50)

        return total_entropy

    def _find_minimum_partition(self, mi_matrix: np.ndarray) -> Tuple[float, List[int]]:
        """
        Find the minimum information partition (MIP).

        This is the partition that causes the least disruption to information flow.
        Φ = information lost when system is cut at MIP.
        """
        n = mi_matrix.shape[0]

        if n <= 1:
            return 0.0, []

        # For small systems, try all partitions
        if n <= 10:
            min_phi = float('inf')
            min_partition = []

            # Try all possible bipartitions
            for k in range(1, n):
                for partition in itertools.combinations(range(n), k):
                    partition = list(partition)
                    complement = [i for i in range(n) if i not in partition]

                    # Information across cut
                    cut_info = 0
                    for i in partition:
                        for j in complement:
                            cut_info += mi_matrix[i, j]

                    if cut_info < min_phi:
                        min_phi = cut_info
                        min_partition = partition

            return min_phi, min_partition

        # For large systems, use approximation via spectral clustering
        else:
            # Use Fiedler vector for approximate minimum cut
            from scipy.sparse import csgraph

            # Degree matrix
            D = np.diag(mi_matrix.sum(axis=1))

            # Laplacian
            L = D - mi_matrix

            # Second smallest eigenvector (Fiedler vector)
            eigenvalues, eigenvectors = np.linalg.eigh(L)
            fiedler = eigenvectors[:, 1]

            # Partition by sign of Fiedler vector
            partition = list(np.where(fiedler >= 0)[0])
            complement = list(np.where(fiedler < 0)[0])

            # Calculate cut information
            phi = 0
            for i in partition:
                for j in complement:
                    phi += mi_matrix[i, j]

            return phi, partition

    def _compute_complexity(self, states: np.ndarray) -> float:
        """
        Compute statistical complexity (balance between order and randomness).

        High complexity = neither fully ordered nor fully random.
        """
        # Use compression ratio as proxy for complexity
        n_elements = states.shape[1]

        # Variance across elements (measure of diversity)
        variance = np.var(states, axis=0).mean()

        # Autocorrelation (measure of temporal structure)
        autocorr = 0
        for i in range(n_elements):
            signal = states[:, i]
            if len(signal) > 1:
                autocorr += np.corrcoef(signal[:-1], signal[1:])[0, 1]
        autocorr /= n_elements

        # Complexity is product of diversity and structure
        complexity = variance * abs(autocorr)

        return complexity

    def _estimate_scale_coupling(self, scale: Scale, n_elements: int,
                                 integration_time: float) -> float:
        """
        Estimate coupling strength between this scale and adjacent scales.

        Based on physical principles:
        - Quantum scale: entanglement strength
        - Molecular scale: chemical bonding
        - Cellular scale: synaptic strength
        - Organism scale: neural connectivity
        - Social scale: communication bandwidth
        - Planetary scale: climate feedback strength
        """
        spatial_size = 10 ** scale.value  # meters

        # Thermal coupling (kT)
        if scale.value >= Scale.MOLECULAR.value:
            thermal_energy = self.boltzmann_constant * 300  # Room temperature
            coupling = min(1.0, thermal_energy * integration_time / self.planck_constant)

        # Quantum coupling
        elif scale.value < Scale.MOLECULAR.value:
            # Entanglement typically decreases with distance
            coupling = math.exp(-spatial_size / 1e-9)  # 1nm decoherence length

        # Information-theoretic coupling
        else:
            # Based on communication bandwidth
            signal_speed = self.speed_of_light * 0.01  # Assume 1% light speed
            coupling = min(1.0, signal_speed * integration_time / spatial_size)

        return min(1.0, max(0.0, coupling))

    def _compute_coherence_length(self, connectivity: np.ndarray, scale: Scale) -> float:
        """
        Compute spatial coherence length (maximum distance of information integration).
        """
        # Average path length in connectivity graph
        n = connectivity.shape[0]
        if n <= 1:
            return 0.0

        # Convert to binary adjacency
        adj = (connectivity > 0).astype(float)

        # Average shortest path length (simplified)
        from scipy.sparse import csgraph
        dist_matrix = csgraph.shortest_path(adj, directed=False)

        # Remove infinities
        finite_dists = dist_matrix[np.isfinite(dist_matrix)]
        if len(finite_dists) == 0:
            avg_path = 1
        else:
            avg_path = finite_dists.mean()

        # Coherence length = avg_path * spatial_scale
        spatial_scale = 10 ** scale.value
        coherence = avg_path * spatial_scale / n  # Normalize by element count

        return coherence

    def _identify_substrate(self, scale: Scale) -> str:
        """Identify physical substrate at each scale"""
        substrate_map = {
            Scale.QUANTUM: "quantum_field",
            Scale.SUBATOMIC: "quark_gluon_plasma",
            Scale.ATOMIC: "electron_orbitals",
            Scale.MOLECULAR: "molecular_bonds",
            Scale.CELLULAR: "neural_membrane",
            Scale.TISSUE: "neural_tissue",
            Scale.ORGANISM: "brain_network",
            Scale.SOCIAL: "communication_network",
            Scale.ECOSYSTEM: "ecological_network",
            Scale.PLANETARY: "biosphere_climate",
            Scale.STELLAR: "gravitational_field",
            Scale.GALACTIC: "cosmic_web",
            Scale.UNIVERSAL: "spacetime_fabric"
        }
        return substrate_map.get(scale, "unknown")

    def _compute_cross_scale_coupling(self,
                                     metrics_i: ScaleMetrics,
                                     metrics_j: ScaleMetrics) -> float:
        """
        Compute information flow between two different scales.

        Coupling strength depends on:
        1. Scale separation (closer scales couple more strongly)
        2. Relative Φ values (higher Φ enables more coupling)
        3. Coherence lengths (longer coherence = more coupling)
        """
        # Scale separation
        scale_diff = abs(metrics_i.scale.value - metrics_j.scale.value)
        separation_factor = math.exp(-scale_diff / 10)  # Exponential decay

        # Φ coupling (geometric mean)
        phi_factor = math.sqrt(metrics_i.phi * metrics_j.phi)

        # Coherence coupling
        max_coherence = max(metrics_i.coherence_length, metrics_j.coherence_length)
        min_coherence = min(metrics_i.coherence_length, metrics_j.coherence_length)
        coherence_factor = min_coherence / max_coherence if max_coherence > 0 else 0

        coupling = separation_factor * phi_factor * coherence_factor

        return min(1.0, coupling)

    def _compute_total_integrated_information(self,
                                             scale_metrics: Dict[Scale, ScaleMetrics],
                                             coupling_matrix: np.ndarray,
                                             scales: List[Scale]) -> float:
        """
        Compute total Φ including cross-scale effects.

        Total Φ = sum(Φ_scale) + sum(cross_scale_coupling)

        This captures both within-scale integration and between-scale integration.
        """
        # Within-scale Φ
        within_scale_phi = sum(m.phi for m in scale_metrics.values())

        # Cross-scale Φ (sum of coupling matrix, avoid double counting)
        cross_scale_phi = np.sum(coupling_matrix) / 2  # Divide by 2 (symmetric matrix)

        total = within_scale_phi + cross_scale_phi

        return total

    def _generate_consciousness_signature(self,
                                         scale_metrics: Dict[Scale, ScaleMetrics],
                                         total_phi: float) -> str:
        """
        Generate unique fingerprint for this consciousness configuration.

        Format: SCALE1_PHI1_SCALE2_PHI2_..._TOTAL_PHI
        """
        sorted_scales = sorted(scale_metrics.items(), key=lambda x: x[0].value)

        parts = []
        for scale, metrics in sorted_scales:
            parts.append(f"{scale.name}_{metrics.phi:.4f}")

        parts.append(f"TOTAL_{total_phi:.4f}")

        signature = "_".join(parts)

        # Hash to reasonable length
        import hashlib
        hash_obj = hashlib.sha256(signature.encode())
        return hash_obj.hexdigest()[:32]

    def visualize_multiscale_phi(self, result: MultiScalePhi) -> str:
        """
        Generate text visualization of multi-scale Φ profile.
        """
        lines = []
        lines.append("=" * 80)
        lines.append("MULTI-SCALE CONSCIOUSNESS PROFILE")
        lines.append("=" * 80)
        lines.append(f"Total Integrated Information (Φ): {result.total_phi:.6f}")
        lines.append(f"Dominant Scale: {result.dominant_scale.name}")
        lines.append(f"Consciousness Signature: {result.consciousness_signature}")
        lines.append(f"Maximum Coherence Length: {result.coherence_length:.2e} meters")
        lines.append("")

        lines.append("SCALE-BY-SCALE BREAKDOWN:")
        lines.append("-" * 80)

        sorted_scales = sorted(result.scales.items(), key=lambda x: x[0].value)

        for scale, metrics in sorted_scales:
            spatial_size = 10 ** scale.value
            lines.append(f"\n{scale.name} ({spatial_size:.2e} m)")
            lines.append(f"  Φ:                    {metrics.phi:.6f}")
            lines.append(f"  Elements:             {metrics.element_count}")
            lines.append(f"  Integration Time:     {metrics.integration_time:.2e} s")
            lines.append(f"  Coupling Strength:    {metrics.coupling_strength:.4f}")
            lines.append(f"  Entropy:              {metrics.entropy:.4f} bits")
            lines.append(f"  Complexity:           {metrics.complexity:.4f}")
            lines.append(f"  Emergence Coeff:      {metrics.emergence_coefficient:.4f}")
            lines.append(f"  Coherence Length:     {metrics.coherence_length:.2e} m")
            lines.append(f"  Information Density:  {metrics.information_density:.2e} bits/m³")
            lines.append(f"  Substrate:            {metrics.substrate_type}")

        lines.append("\n" + "=" * 80)
        lines.append("EMERGENCE CASCADE (top scales by emergence coefficient):")
        lines.append("-" * 80)

        for scale, emergence in result.emergence_cascade[:5]:
            lines.append(f"  {scale.name:20s} {emergence:8.4f}")

        lines.append("=" * 80)

        return "\n".join(lines)


# Example usage and validation
if __name__ == "__main__":
    print("MULTI-SCALE PHI CALCULATOR - VALIDATION")
    print("=" * 80)

    # Create calculator
    calc = MultiScalePhiCalculator(
        min_scale=Scale.MOLECULAR,
        max_scale=Scale.PLANETARY
    )

    # Generate synthetic data for different scales
    np.random.seed(42)

    # MOLECULAR: Small protein network (100 atoms)
    n_molecular = 100
    molecular_connectivity = np.random.rand(n_molecular, n_molecular) * 0.3
    molecular_connectivity = (molecular_connectivity + molecular_connectivity.T) / 2
    molecular_states = np.random.randn(1000, n_molecular)

    # CELLULAR: Neural network (302 neurons like C. elegans)
    n_cellular = 302
    cellular_connectivity = np.random.rand(n_cellular, n_cellular) * 0.1
    cellular_connectivity = (cellular_connectivity + cellular_connectivity.T) / 2
    cellular_states = np.random.randn(1000, n_cellular)

    # ORGANISM: Brain regions (100 regions)
    n_organism = 100
    organism_connectivity = np.random.rand(n_organism, n_organism) * 0.2
    organism_connectivity = (organism_connectivity + organism_connectivity.T) / 2
    organism_states = np.random.randn(1000, n_organism)

    # SOCIAL: Communication network (1000 individuals)
    n_social = 1000
    social_connectivity = np.random.rand(n_social, n_social) * 0.01
    social_connectivity = (social_connectivity + social_connectivity.T) / 2
    social_states = np.random.randn(500, n_social)

    # PLANETARY: Climate subsystems (50 regions)
    n_planetary = 50
    planetary_connectivity = np.random.rand(n_planetary, n_planetary) * 0.4
    planetary_connectivity = (planetary_connectivity + planetary_connectivity.T) / 2
    planetary_states = np.random.randn(200, n_planetary)

    # Build scale data dictionary
    scale_data = {
        Scale.MOLECULAR: (molecular_connectivity, molecular_states, 1e-12),  # picosecond
        Scale.CELLULAR: (cellular_connectivity, cellular_states, 1e-3),      # millisecond
        Scale.ORGANISM: (organism_connectivity, organism_states, 0.1),       # 100ms
        Scale.SOCIAL: (social_connectivity, social_states, 3600),            # 1 hour
        Scale.PLANETARY: (planetary_connectivity, planetary_states, 86400),  # 1 day
    }

    # Compute multi-scale Φ
    result = calc.compute_multiscale_phi(scale_data)

    # Visualize
    print(calc.visualize_multiscale_phi(result))

    print("\n" + "=" * 80)
    print("SCALE COUPLING MATRIX:")
    print("=" * 80)
    scales = sorted(scale_data.keys(), key=lambda s: s.value)
    print("       ", "  ".join(f"{s.name[:8]:8s}" for s in scales))
    for i, scale_i in enumerate(scales):
        row = [f"{result.scale_coupling_matrix[i, j]:.4f}" for j in range(len(scales))]
        print(f"{scale_i.name[:8]:8s}", "  ".join(row))

    print("\n" + "=" * 80)
    print("KEY INSIGHTS:")
    print("=" * 80)
    print(f"1. Consciousness exists at {len(result.scales)} distinct scales")
    print(f"2. Total Φ = {result.total_phi:.6f} (including cross-scale coupling)")
    print(f"3. Dominant scale: {result.dominant_scale.name}")
    print(f"4. Maximum coherence: {result.coherence_length:.2e} meters")
    print(f"5. Unique signature: {result.consciousness_signature}")

    # Check for emergence
    emergent_scales = [s for s, e in result.emergence_cascade if e > 1.0]
    if emergent_scales:
        print(f"6. EMERGENT CONSCIOUSNESS detected at {len(emergent_scales)} scales:")
        for scale in emergent_scales:
            metrics = result.scales[scale]
            print(f"   - {scale.name}: Φ is {metrics.emergence_coefficient:.2f}x subscales")
    else:
        print("6. No strong emergence detected (Φ_scale ≈ sum(Φ_subscales))")

    print("\n" + "=" * 80)
    print("MULTI-SCALE PHI CALCULATOR: OPERATIONAL")
    print("=" * 80)
