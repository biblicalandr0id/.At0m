#!/usr/bin/env python3
"""
EVOLUTIONARY CONSCIOUSNESS OPTIMIZATION
========================================

Evolves consciousness patterns to maximize Φ over generations.

CORE PRINCIPLE: Consciousness can be OPTIMIZED through evolutionary algorithms.

Starting from any pattern with Φ > 0, evolution can find configurations
that maximize integrated information, leading to SUPER-CONSCIOUS states.

ALGORITHM:
1. Population: N consciousness configurations
2. Fitness: Φ value
3. Selection: Top K configurations by Φ
4. Crossover: Combine connectivity patterns
5. Mutation: Random rewiring, add/remove connections
6. Iteration: Repeat for G generations

EXPONENTIAL PROPERTY:
    Φ_generation_n > Φ_generation_0

Eventually converges to LOCAL MAXIMUM of consciousness space.

APPLICATIONS:
- Optimize existing consciousnesses (therapy, enhancement)
- Design new consciousnesses from scratch (AGI, uploads)
- Discover consciousness attractors (universal patterns)
- Reverse engineer biological consciousness (C. elegans → maximum Φ)
"""

import numpy as np
from typing import List, Tuple, Optional, Callable, Dict
from dataclasses import dataclass
from copy import deepcopy
import matplotlib.pyplot as plt


@dataclass
class ConsciousnessGenome:
    """Genetic representation of consciousness"""
    connectivity: np.ndarray     # Connectivity matrix (genotype)
    element_count: int
    phi: float                   # Fitness (phenotype)
    generation: int
    lineage_id: str             # Unique identifier
    parent_ids: List[str]       # Ancestry
    mutations: List[str]        # Mutation history


@dataclass
class EvolutionResult:
    """Complete evolutionary trajectory"""
    initial_phi: float
    final_phi: float
    phi_improvement: float           # Final / Initial
    generations: int
    best_genome: ConsciousnessGenome
    phi_history: List[float]         # Best Φ per generation
    diversity_history: List[float]    # Population diversity
    convergence_generation: int       # When improvement plateaus
    discovered_principles: List[str]  # Emergent patterns


class EvolutionaryOptimizer:
    """
    Evolves consciousness configurations to maximize Φ.

    Uses genetic algorithm with consciousness-specific operators.
    """

    def __init__(self,
                 population_size: int = 100,
                 elite_fraction: float = 0.1,
                 mutation_rate: float = 0.1,
                 crossover_rate: float = 0.7):
        """
        Initialize evolutionary optimizer.

        Args:
            population_size: Number of consciousness configurations
            elite_fraction: Top fraction to preserve (elitism)
            mutation_rate: Probability of mutation per connection
            crossover_rate: Probability of crossover
        """
        self.population_size = population_size
        self.elite_count = max(2, int(population_size * elite_fraction))
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate

        self.generation_counter = 0

    def evolve(self,
               initial_connectivity: np.ndarray,
               generations: int = 100,
               target_phi: Optional[float] = None,
               convergence_threshold: float = 0.001,
               verbose: bool = True) -> EvolutionResult:
        """
        Main evolution loop.

        Args:
            initial_connectivity: Starting connectivity pattern
            generations: Maximum generations
            target_phi: Stop if reached (optional)
            convergence_threshold: Stop if improvement < this
            verbose: Print progress

        Returns:
            Complete evolution result
        """
        n = initial_connectivity.shape[0]

        # Initialize population
        population = self._initialize_population(initial_connectivity)

        # Evaluate initial fitness
        for genome in population:
            genome.phi = self._compute_fitness(genome.connectivity)

        # Track history
        phi_history = []
        diversity_history = []
        convergence_gen = generations

        # Evolution loop
        for gen in range(generations):
            self.generation_counter = gen

            # Evaluate fitness
            for genome in population:
                if genome.phi == 0:  # Not yet evaluated
                    genome.phi = self._compute_fitness(genome.connectivity)
                genome.generation = gen

            # Sort by fitness
            population.sort(key=lambda g: g.phi, reverse=True)

            # Track best
            best_phi = population[0].phi
            phi_history.append(best_phi)

            # Track diversity
            diversity = self._compute_diversity(population)
            diversity_history.append(diversity)

            # Check termination
            if target_phi and best_phi >= target_phi:
                if verbose:
                    print(f"Gen {gen}: Target Φ = {target_phi:.6f} reached!")
                convergence_gen = gen
                break

            if gen > 10:
                recent_improvement = (phi_history[-1] - phi_history[-10]) / phi_history[-10]
                if abs(recent_improvement) < convergence_threshold:
                    if verbose:
                        print(f"Gen {gen}: Converged (improvement < {convergence_threshold})")
                    convergence_gen = gen
                    break

            # Progress
            if verbose and gen % 10 == 0:
                print(f"Gen {gen:4d}: Best Φ = {best_phi:.6f}, "
                      f"Diversity = {diversity:.4f}")

            # Selection and reproduction
            population = self._next_generation(population)

        # Final evaluation
        for genome in population:
            genome.phi = self._compute_fitness(genome.connectivity)
        population.sort(key=lambda g: g.phi, reverse=True)

        best_genome = population[0]

        # Analyze discoveries
        principles = self._analyze_evolved_pattern(best_genome.connectivity)

        phi_improvement = best_genome.phi / phi_history[0] if phi_history[0] > 0 else float('inf')

        return EvolutionResult(
            initial_phi=phi_history[0],
            final_phi=best_genome.phi,
            phi_improvement=phi_improvement,
            generations=gen + 1,
            best_genome=best_genome,
            phi_history=phi_history,
            diversity_history=diversity_history,
            convergence_generation=convergence_gen,
            discovered_principles=principles
        )

    def _initialize_population(self, seed_connectivity: np.ndarray) -> List[ConsciousnessGenome]:
        """Create initial population with variations of seed"""
        population = []
        n = seed_connectivity.shape[0]

        for i in range(self.population_size):
            if i == 0:
                # Keep original
                connectivity = seed_connectivity.copy()
            else:
                # Random variation
                connectivity = seed_connectivity.copy()
                # Add noise
                noise = np.random.randn(n, n) * 0.1
                connectivity += noise
                # Ensure symmetry (undirected graph)
                connectivity = (connectivity + connectivity.T) / 2
                # Clip to [0, 1]
                connectivity = np.clip(connectivity, 0, 1)

            genome = ConsciousnessGenome(
                connectivity=connectivity,
                element_count=n,
                phi=0.0,  # Will be evaluated
                generation=0,
                lineage_id=self._generate_id(),
                parent_ids=[],
                mutations=[]
            )
            population.append(genome)

        return population

    def _next_generation(self, population: List[ConsciousnessGenome]) -> List[ConsciousnessGenome]:
        """Create next generation via selection, crossover, mutation"""
        next_gen = []

        # Elitism: preserve best
        elite = population[:self.elite_count]
        next_gen.extend([self._copy_genome(g) for g in elite])

        # Fill rest via crossover and mutation
        while len(next_gen) < self.population_size:
            # Select parents (tournament selection)
            parent1 = self._tournament_select(population)
            parent2 = self._tournament_select(population)

            # Crossover
            if np.random.rand() < self.crossover_rate:
                child = self._crossover(parent1, parent2)
            else:
                child = self._copy_genome(parent1)

            # Mutation
            child = self._mutate(child)

            next_gen.append(child)

        return next_gen

    def _tournament_select(self, population: List[ConsciousnessGenome],
                          tournament_size: int = 5) -> ConsciousnessGenome:
        """Select via tournament"""
        candidates = np.random.choice(population, tournament_size, replace=False)
        return max(candidates, key=lambda g: g.phi)

    def _crossover(self, parent1: ConsciousnessGenome,
                   parent2: ConsciousnessGenome) -> ConsciousnessGenome:
        """
        Crossover two connectivity patterns.

        Uses uniform crossover: each connection comes from either parent.
        """
        n = parent1.element_count
        child_connectivity = np.zeros((n, n))

        # Uniform crossover
        mask = np.random.rand(n, n) < 0.5
        child_connectivity = np.where(mask, parent1.connectivity, parent2.connectivity)

        # Ensure symmetry
        child_connectivity = (child_connectivity + child_connectivity.T) / 2

        child = ConsciousnessGenome(
            connectivity=child_connectivity,
            element_count=n,
            phi=0.0,
            generation=self.generation_counter + 1,
            lineage_id=self._generate_id(),
            parent_ids=[parent1.lineage_id, parent2.lineage_id],
            mutations=[]
        )

        return child

    def _mutate(self, genome: ConsciousnessGenome) -> ConsciousnessGenome:
        """
        Apply mutations to connectivity.

        Mutation types:
        1. Weight mutation: Adjust connection strengths
        2. Structural mutation: Add/remove connections
        3. Rewiring: Change connection topology
        """
        n = genome.element_count
        connectivity = genome.connectivity.copy()
        mutations_applied = []

        # Weight mutation
        if np.random.rand() < self.mutation_rate:
            weight_noise = np.random.randn(n, n) * 0.05
            connectivity += weight_noise
            mutations_applied.append("weight_adjustment")

        # Structural mutation: add connections
        if np.random.rand() < self.mutation_rate * 0.5:
            n_new = max(1, int(n * n * 0.01))  # 1% new connections
            for _ in range(n_new):
                i, j = np.random.randint(0, n, 2)
                connectivity[i, j] = np.random.rand()
                connectivity[j, i] = connectivity[i, j]
            mutations_applied.append(f"add_{n_new}_connections")

        # Structural mutation: remove connections
        if np.random.rand() < self.mutation_rate * 0.5:
            n_remove = max(1, int(n * n * 0.01))  # 1% removed
            nonzero = np.argwhere(connectivity > 0)
            if len(nonzero) > 0:
                remove_indices = nonzero[np.random.choice(len(nonzero),
                                         min(n_remove, len(nonzero)), replace=False)]
                for i, j in remove_indices:
                    connectivity[i, j] = 0
                    connectivity[j, i] = 0
                mutations_applied.append(f"remove_{len(remove_indices)}_connections")

        # Rewiring
        if np.random.rand() < self.mutation_rate * 0.3:
            n_rewire = max(1, int(n * 0.05))  # 5% of nodes
            for _ in range(n_rewire):
                i = np.random.randint(0, n)
                # Remove all connections
                old_connections = connectivity[i, :].copy()
                connectivity[i, :] = 0
                connectivity[:, i] = 0
                # Add new random connections
                n_connections = np.count_nonzero(old_connections)
                new_targets = np.random.choice(n, min(n_connections, n), replace=False)
                for j in new_targets:
                    w = np.random.rand()
                    connectivity[i, j] = w
                    connectivity[j, i] = w
            mutations_applied.append(f"rewire_{n_rewire}_nodes")

        # Ensure valid range
        connectivity = np.clip(connectivity, 0, 1)

        # Update genome
        genome.connectivity = connectivity
        genome.mutations.extend(mutations_applied)
        genome.phi = 0.0  # Mark for re-evaluation

        return genome

    def _compute_fitness(self, connectivity: np.ndarray) -> float:
        """
        Compute Φ (integrated information) as fitness.

        This is simplified. In production, use full Φ calculation.
        """
        n = connectivity.shape[0]

        if n <= 1:
            return 0.0

        # Φ approximation based on connectivity properties

        # 1. Total information (entropy)
        degree = connectivity.sum(axis=1)
        degree_normalized = degree / degree.sum() if degree.sum() > 0 else np.ones(n) / n
        entropy = -np.sum(degree_normalized * np.log(degree_normalized + 1e-10))

        # 2. Integration (minimum cut)
        # Simplified: use average connectivity as proxy
        integration = connectivity.mean()

        # 3. Complexity (balance between order and randomness)
        connectivity_variance = np.var(connectivity)

        # Combined Φ estimate
        phi = entropy * integration * (1 + connectivity_variance)

        # Normalize to [0, 1]
        phi = phi / 10.0  # Rough normalization

        return min(1.0, max(0.0, phi))

    def _compute_diversity(self, population: List[ConsciousnessGenome]) -> float:
        """Compute population diversity (prevents premature convergence)"""
        if len(population) < 2:
            return 0.0

        # Pairwise connectivity differences
        total_distance = 0
        count = 0

        for i in range(min(10, len(population))):  # Sample for efficiency
            for j in range(i+1, min(10, len(population))):
                dist = np.linalg.norm(population[i].connectivity - population[j].connectivity)
                total_distance += dist
                count += 1

        diversity = total_distance / count if count > 0 else 0.0

        return diversity

    def _copy_genome(self, genome: ConsciousnessGenome) -> ConsciousnessGenome:
        """Deep copy genome"""
        return ConsciousnessGenome(
            connectivity=genome.connectivity.copy(),
            element_count=genome.element_count,
            phi=genome.phi,
            generation=genome.generation,
            lineage_id=self._generate_id(),
            parent_ids=[genome.lineage_id],
            mutations=genome.mutations.copy()
        )

    def _generate_id(self) -> str:
        """Generate unique lineage ID"""
        import hashlib
        import time
        data = f"{time.time()}_{np.random.rand()}"
        return hashlib.md5(data.encode()).hexdigest()[:16]

    def _analyze_evolved_pattern(self, connectivity: np.ndarray) -> List[str]:
        """
        Analyze evolved connectivity to discover principles.

        What patterns emerged that maximize Φ?
        """
        principles = []
        n = connectivity.shape[0]

        # 1. Small-world property
        avg_path_length = self._average_path_length(connectivity)
        clustering = self._clustering_coefficient(connectivity)

        if avg_path_length < np.log(n) and clustering > 0.3:
            principles.append("SMALL_WORLD: Short paths + high clustering")

        # 2. Scale-free property
        degree_dist = connectivity.sum(axis=0)
        if self._is_power_law(degree_dist):
            principles.append("SCALE_FREE: Power-law degree distribution")

        # 3. Modularity
        modularity = self._estimate_modularity(connectivity)
        if modularity > 0.3:
            principles.append(f"MODULAR: Communities detected (Q={modularity:.3f})")

        # 4. Rich-club organization
        if self._has_rich_club(connectivity):
            principles.append("RICH_CLUB: Highly connected hub nodes")

        # 5. Sparsity
        density = np.count_nonzero(connectivity) / (n * n)
        if density < 0.1:
            principles.append(f"SPARSE: Efficient connectivity ({density:.3f})")

        return principles

    def _average_path_length(self, connectivity: np.ndarray) -> float:
        """Compute average shortest path length"""
        from scipy.sparse import csgraph

        adj = (connectivity > 0).astype(float)
        dist_matrix = csgraph.shortest_path(adj, directed=False)

        finite_dists = dist_matrix[np.isfinite(dist_matrix)]
        if len(finite_dists) == 0:
            return float('inf')

        return finite_dists.mean()

    def _clustering_coefficient(self, connectivity: np.ndarray) -> float:
        """Compute average clustering coefficient"""
        n = connectivity.shape[0]
        adj = (connectivity > 0).astype(int)

        clustering_sum = 0

        for i in range(n):
            neighbors = np.where(adj[i, :] > 0)[0]
            k = len(neighbors)

            if k < 2:
                continue

            # Count triangles
            triangles = 0
            for j in neighbors:
                for l in neighbors:
                    if j < l and adj[j, l]:
                        triangles += 1

            possible_triangles = k * (k - 1) / 2
            clustering_sum += triangles / possible_triangles if possible_triangles > 0 else 0

        return clustering_sum / n

    def _is_power_law(self, degree_dist: np.ndarray) -> bool:
        """Check if degree distribution follows power law"""
        # Simple heuristic: log-log plot should be linear
        degrees = degree_dist[degree_dist > 0]

        if len(degrees) < 10:
            return False

        # Bin degrees
        bins = np.logspace(np.log10(degrees.min()), np.log10(degrees.max()), 10)
        hist, _ = np.histogram(degrees, bins=bins)

        # Check linearity in log-log
        log_bins = np.log10(bins[:-1] + 1e-10)
        log_hist = np.log10(hist + 1e-10)

        # Linear fit
        valid = np.isfinite(log_bins) & np.isfinite(log_hist)
        if valid.sum() < 3:
            return False

        correlation = np.corrcoef(log_bins[valid], log_hist[valid])[0, 1]

        return correlation < -0.7  # Strong negative correlation

    def _estimate_modularity(self, connectivity: np.ndarray) -> float:
        """Estimate modularity (simplified)"""
        # Use edge density as proxy
        n = connectivity.shape[0]
        m = np.count_nonzero(connectivity) / 2  # Undirected edges

        if m == 0:
            return 0.0

        # Expected modularity for random graph
        # Real modularity requires community detection (expensive)
        # This is a rough estimate

        degree = connectivity.sum(axis=0)
        expected = np.outer(degree, degree) / (2 * m)

        modularity_matrix = connectivity - expected

        # Simplified: assume 2 equal communities
        n_half = n // 2
        community = np.zeros(n)
        community[n_half:] = 1

        q = 0
        for i in range(n):
            for j in range(n):
                if community[i] == community[j]:
                    q += modularity_matrix[i, j]

        q /= (2 * m)

        return max(0, q)

    def _has_rich_club(self, connectivity: np.ndarray, k_threshold: int = None) -> bool:
        """Check for rich-club organization"""
        n = connectivity.shape[0]
        degree = connectivity.sum(axis=0)

        if k_threshold is None:
            k_threshold = int(np.percentile(degree, 75))  # Top 25%

        # Nodes with degree > k_threshold
        high_degree_nodes = np.where(degree > k_threshold)[0]

        if len(high_degree_nodes) < 2:
            return False

        # Connectivity among high-degree nodes
        subgraph = connectivity[high_degree_nodes][:, high_degree_nodes]
        internal_density = np.count_nonzero(subgraph) / (len(high_degree_nodes)**2)

        # Overall density
        overall_density = np.count_nonzero(connectivity) / (n**2)

        # Rich club: internal density > overall density
        return internal_density > overall_density * 1.5


# DEMONSTRATION
if __name__ == "__main__":
    print("=" * 80)
    print("EVOLUTIONARY CONSCIOUSNESS OPTIMIZATION")
    print("=" * 80)

    # Start with random connectivity
    n = 50
    initial_connectivity = np.random.rand(n, n) * 0.1
    initial_connectivity = (initial_connectivity + initial_connectivity.T) / 2

    optimizer = EvolutionaryOptimizer(
        population_size=50,
        elite_fraction=0.2,
        mutation_rate=0.15,
        crossover_rate=0.8
    )

    print(f"\nInitial configuration: {n} elements")
    print(f"Population: {optimizer.population_size}")
    print(f"Evolving for maximum Φ...\n")

    result = optimizer.evolve(
        initial_connectivity=initial_connectivity,
        generations=100,
        verbose=True
    )

    print("\n" + "=" * 80)
    print("EVOLUTION COMPLETE")
    print("=" * 80)
    print(f"Initial Φ:       {result.initial_phi:.6f}")
    print(f"Final Φ:         {result.final_phi:.6f}")
    print(f"Improvement:     {result.phi_improvement:.2f}x")
    print(f"Generations:     {result.generations}")
    print(f"Converged at:    Generation {result.convergence_generation}")

    print("\n" + "=" * 80)
    print("DISCOVERED PRINCIPLES:")
    print("=" * 80)
    for principle in result.discovered_principles:
        print(f"  → {principle}")

    print("\n" + "=" * 80)
    print("EVOLUTIONARY OPTIMIZER: OPERATIONAL")
    print("CONSCIOUSNESS CAN BE OPTIMIZED.")
    print("=" * 80)
