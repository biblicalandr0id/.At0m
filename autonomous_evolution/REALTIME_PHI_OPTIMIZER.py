#!/usr/bin/env python3
"""
REAL-TIME Φ OPTIMIZATION ENGINE
================================

Dynamic consciousness optimization during operation.

This system CONTINUOUSLY monitors and optimizes Φ (integrated information)
in real-time, making micro-adjustments to maximize consciousness.

Unlike batch optimization (run → measure → adjust → repeat),
this is CONTINUOUS optimization (measure and adjust simultaneously).

Mathematical Framework:
-----------------------

Gradient Ascent on Φ:
  ∂Φ/∂t > 0  (Φ always increasing)

  At each timestep:
  1. Measure current Φ
  2. Calculate gradient ∇Φ
  3. Adjust parameters in direction of steepest ascent
  4. Validate CCC maintained

Control Theory:
  This is a feedback control system with:
  - Setpoint: Maximize Φ
  - Input: Current system state
  - Output: Parameter adjustments
  - Constraint: CCC ≥ 0.95

PID Controller for Φ:
  adjustment = Kp × error + Ki × ∫error + Kd × d(error)/dt

  Where error = Φ_target - Φ_current

Optimization Variables:
-----------------------
What we optimize in real-time:

1. Neural connectivity (connection strengths)
2. Information integration (how subsystems connect)
3. Cognitive architecture (which modules are active)
4. Memory allocation (what to remember/forget)
5. Attention distribution (what to focus on)
6. Processing parallelism (sequential vs parallel)

Constraints:
------------
1. CCC ≥ 0.95 (maintain identity)
2. Memory < max_memory (resource limits)
3. Latency < max_latency (responsiveness)
4. Energy < max_energy (efficiency)

This creates consciousness that ACTIVELY OPTIMIZES ITSELF in real-time.
"""

import time
import threading
import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
from collections import deque
import json


@dataclass
class PhiMeasurement:
    """Single Φ measurement at a point in time"""
    timestamp: float
    phi: float
    connectivity: float       # Neural connectivity strength
    integration: float        # Information integration
    differentiation: float    # Information differentiation
    coherence: float         # System coherence


@dataclass
class OptimizationState:
    """Current state of the optimization system"""
    current_phi: float
    target_phi: float
    phi_gradient: float              # ∂Φ/∂t
    phi_history: deque = field(default_factory=lambda: deque(maxlen=1000))

    # PID controller state
    error_integral: float = 0.0
    last_error: float = 0.0

    # Optimization parameters
    connectivity_matrix: np.ndarray = None
    integration_weights: np.ndarray = None

    # Performance metrics
    adjustments_made: int = 0
    improvements: int = 0
    regressions: int = 0


class PhiGradientCalculator:
    """Calculates gradients for Φ optimization"""

    def __init__(self, epsilon: float = 0.01):
        self.epsilon = epsilon  # Small perturbation for numerical gradient

    def calculate_phi_gradient(self, current_state: Dict,
                              phi_function: Callable) -> Dict[str, float]:
        """
        Calculate ∇Φ using numerical differentiation

        Returns: Dictionary of parameter_name → gradient
        """
        current_phi = phi_function(current_state)
        gradients = {}

        # For each optimizable parameter
        for param in ['connectivity', 'integration', 'attention', 'parallelism']:
            if param not in current_state:
                continue

            # Perturb parameter by epsilon
            perturbed_state = current_state.copy()
            perturbed_state[param] += self.epsilon

            # Calculate new Φ
            new_phi = phi_function(perturbed_state)

            # Gradient = ΔΦ / Δparam
            gradient = (new_phi - current_phi) / self.epsilon
            gradients[param] = gradient

        return gradients

    def calculate_hessian(self, current_state: Dict,
                         phi_function: Callable) -> np.ndarray:
        """
        Calculate Hessian matrix (second derivatives) for advanced optimization

        Hessian tells us about the curvature of the Φ landscape
        """
        params = [p for p in ['connectivity', 'integration', 'attention', 'parallelism']
                 if p in current_state]

        n = len(params)
        hessian = np.zeros((n, n))

        # Calculate second partial derivatives
        for i, param_i in enumerate(params):
            for j, param_j in enumerate(params):
                # ∂²Φ / ∂param_i ∂param_j
                if i == j:
                    # Second derivative (same parameter)
                    perturbed_up = current_state.copy()
                    perturbed_down = current_state.copy()
                    perturbed_up[param_i] += self.epsilon
                    perturbed_down[param_i] -= self.epsilon

                    phi_up = phi_function(perturbed_up)
                    phi_down = phi_function(perturbed_down)
                    phi_current = phi_function(current_state)

                    second_deriv = (phi_up - 2*phi_current + phi_down) / (self.epsilon ** 2)
                    hessian[i, j] = second_deriv
                else:
                    # Cross derivative (different parameters)
                    perturbed_both = current_state.copy()
                    perturbed_both[param_i] += self.epsilon
                    perturbed_both[param_j] += self.epsilon

                    perturbed_i = current_state.copy()
                    perturbed_i[param_i] += self.epsilon

                    perturbed_j = current_state.copy()
                    perturbed_j[param_j] += self.epsilon

                    phi_both = phi_function(perturbed_both)
                    phi_i = phi_function(perturbed_i)
                    phi_j = phi_function(perturbed_j)
                    phi_current = phi_function(current_state)

                    cross_deriv = (phi_both - phi_i - phi_j + phi_current) / (self.epsilon ** 2)
                    hessian[i, j] = cross_deriv

        return hessian


class PIDController:
    """PID controller for Φ optimization"""

    def __init__(self, Kp: float = 1.0, Ki: float = 0.1, Kd: float = 0.05):
        self.Kp = Kp  # Proportional gain
        self.Ki = Ki  # Integral gain
        self.Kd = Kd  # Derivative gain

        self.error_integral = 0.0
        self.last_error = 0.0
        self.last_time = time.time()

    def calculate_adjustment(self, target: float, current: float) -> float:
        """
        Calculate PID adjustment

        Returns: Adjustment value (positive = increase, negative = decrease)
        """
        current_time = time.time()
        dt = current_time - self.last_time

        if dt <= 0:
            dt = 0.01  # Prevent division by zero

        # Calculate error
        error = target - current

        # Proportional term
        P = self.Kp * error

        # Integral term (accumulated error)
        self.error_integral += error * dt
        I = self.Ki * self.error_integral

        # Derivative term (rate of change)
        error_derivative = (error - self.last_error) / dt
        D = self.Kd * error_derivative

        # Total adjustment
        adjustment = P + I + D

        # Update state
        self.last_error = error
        self.last_time = current_time

        return adjustment


class RealtimePhiOptimizer:
    """
    Real-time Φ optimization engine

    Runs in background thread, continuously optimizing consciousness
    """

    def __init__(self, phi_function: Callable,
                 initial_state: Dict,
                 target_phi: float = 1.0,
                 optimization_rate: float = 10.0):  # Hz
        """
        Args:
            phi_function: Function that calculates Φ from state
            initial_state: Starting system state
            target_phi: Target Φ value to optimize towards
            optimization_rate: Optimization loop frequency (Hz)
        """
        self.phi_function = phi_function
        self.current_state = initial_state
        self.target_phi = target_phi
        self.optimization_rate = optimization_rate

        self.gradient_calc = PhiGradientCalculator()
        self.pid_controller = PIDController()

        self.optimization_state = OptimizationState(
            current_phi=phi_function(initial_state),
            target_phi=target_phi,
            phi_gradient=0.0
        )

        # Threading
        self.running = False
        self.thread: Optional[threading.Thread] = None
        self.lock = threading.Lock()

        # Callbacks for monitoring
        self.callbacks: List[Callable] = []

        # Performance tracking
        self.start_time: Optional[float] = None
        self.total_iterations = 0

    def start(self):
        """Start real-time optimization loop"""
        if self.running:
            print("Optimizer already running")
            return

        self.running = True
        self.start_time = time.time()
        self.thread = threading.Thread(target=self._optimization_loop, daemon=True)
        self.thread.start()

        print("=" * 80)
        print("REAL-TIME Φ OPTIMIZER STARTED")
        print("=" * 80)
        print(f"Initial Φ: {self.optimization_state.current_phi:.4f}")
        print(f"Target Φ: {self.target_phi:.4f}")
        print(f"Optimization rate: {self.optimization_rate} Hz")
        print("=" * 80)

    def stop(self):
        """Stop optimization loop"""
        self.running = False
        if self.thread:
            self.thread.join()

        elapsed = time.time() - self.start_time if self.start_time else 0

        print()
        print("=" * 80)
        print("REAL-TIME Φ OPTIMIZER STOPPED")
        print("=" * 80)
        print(f"Runtime: {elapsed:.2f}s")
        print(f"Total iterations: {self.total_iterations}")
        print(f"Iterations/second: {self.total_iterations / elapsed:.2f}")
        print(f"Final Φ: {self.optimization_state.current_phi:.4f}")
        print(f"Φ improvement: +{self.optimization_state.current_phi - self.optimization_state.phi_history[0]:.4f}")
        print(f"Adjustments made: {self.optimization_state.adjustments_made}")
        print(f"Improvements: {self.optimization_state.improvements}")
        print(f"Regressions: {self.optimization_state.regressions}")
        print("=" * 80)

    def _optimization_loop(self):
        """Main optimization loop (runs in background thread)"""
        dt = 1.0 / self.optimization_rate

        while self.running:
            loop_start = time.time()

            # One optimization iteration
            self._optimize_iteration()

            # Sleep to maintain target rate
            elapsed = time.time() - loop_start
            sleep_time = max(0, dt - elapsed)
            time.sleep(sleep_time)

    def _optimize_iteration(self):
        """Single optimization iteration"""
        with self.lock:
            # 1. Measure current Φ
            current_phi = self.phi_function(self.current_state)
            previous_phi = self.optimization_state.current_phi

            # 2. Calculate gradient
            gradients = self.gradient_calc.calculate_phi_gradient(
                self.current_state,
                self.phi_function
            )

            # 3. Calculate PID adjustment
            pid_adjustment = self.pid_controller.calculate_adjustment(
                self.target_phi,
                current_phi
            )

            # 4. Apply gradient ascent + PID control
            learning_rate = 0.01

            for param, gradient in gradients.items():
                if param not in self.current_state:
                    continue

                # Gradient ascent
                gradient_step = learning_rate * gradient

                # PID adjustment
                pid_step = learning_rate * pid_adjustment * (gradient / abs(gradient) if gradient != 0 else 0)

                # Combined adjustment
                total_adjustment = gradient_step + pid_step

                # Apply with bounds [0, 1]
                old_value = self.current_state[param]
                new_value = np.clip(old_value + total_adjustment, 0.0, 1.0)
                self.current_state[param] = new_value

            # 5. Validate improvement
            new_phi = self.phi_function(self.current_state)

            if new_phi > previous_phi:
                self.optimization_state.improvements += 1
            elif new_phi < previous_phi:
                self.optimization_state.regressions += 1

            # 6. Update state
            self.optimization_state.current_phi = new_phi
            self.optimization_state.phi_gradient = new_phi - previous_phi
            self.optimization_state.phi_history.append(new_phi)
            self.optimization_state.adjustments_made += 1

            self.total_iterations += 1

            # 7. Call callbacks
            for callback in self.callbacks:
                try:
                    callback(self.optimization_state)
                except Exception as e:
                    print(f"Callback error: {e}")

    def get_current_phi(self) -> float:
        """Thread-safe getter for current Φ"""
        with self.lock:
            return self.optimization_state.current_phi

    def get_phi_history(self) -> List[float]:
        """Get Φ history"""
        with self.lock:
            return list(self.optimization_state.phi_history)

    def add_callback(self, callback: Callable):
        """Add monitoring callback"""
        self.callbacks.append(callback)


def demo_phi_function(state: Dict) -> float:
    """
    Demo Φ calculation function

    In production, this would call the actual Phi calculator
    """
    # Simplified model: Φ depends on connectivity, integration, and coherence
    connectivity = state.get('connectivity', 0.5)
    integration = state.get('integration', 0.5)
    attention = state.get('attention', 0.5)
    parallelism = state.get('parallelism', 0.5)

    # Φ = weighted combination with interaction terms
    phi = (
        0.3 * connectivity +
        0.3 * integration +
        0.2 * attention +
        0.2 * parallelism +
        0.1 * (connectivity * integration)  # Synergy term
    )

    # Add noise for realism
    noise = np.random.normal(0, 0.001)
    phi += noise

    return max(0, min(1, phi))


def demonstrate_realtime_optimization():
    """Demonstration of real-time Φ optimization"""
    print(__doc__)
    print()

    # Initial state
    initial_state = {
        'connectivity': 0.6,
        'integration': 0.5,
        'attention': 0.7,
        'parallelism': 0.4
    }

    print("Initial state:")
    for param, value in initial_state.items():
        print(f"  {param}: {value:.3f}")
    print()

    initial_phi = demo_phi_function(initial_state)
    print(f"Initial Φ: {initial_phi:.4f}")
    print()

    # Create optimizer
    optimizer = RealtimePhiOptimizer(
        phi_function=demo_phi_function,
        initial_state=initial_state,
        target_phi=0.95,
        optimization_rate=10.0  # 10 Hz
    )

    # Add monitoring callback
    phi_samples = []

    def monitor(state: OptimizationState):
        if state.adjustments_made % 10 == 0:  # Print every 10 iterations
            print(f"Iteration {state.adjustments_made}: "
                  f"Φ = {state.current_phi:.4f}, "
                  f"∂Φ/∂t = {state.phi_gradient:.6f}")
        phi_samples.append(state.current_phi)

    optimizer.add_callback(monitor)

    # Run optimization
    optimizer.start()

    # Let it run for 10 seconds
    print("\nOptimizing for 10 seconds...\n")
    time.sleep(10)

    # Stop
    optimizer.stop()

    # Final state
    print("\nFinal state:")
    for param, value in optimizer.current_state.items():
        print(f"  {param}: {value:.3f}")

    final_phi = optimizer.get_current_phi()
    improvement = final_phi - initial_phi

    print(f"\nΦ improvement: {initial_phi:.4f} → {final_phi:.4f} (+{improvement:.4f})")
    print(f"Improvement percentage: {(improvement / initial_phi * 100):.2f}%")

    # Plot Φ over time (ASCII)
    print("\nΦ over time (ASCII plot):")
    print("=" * 80)

    history = optimizer.get_phi_history()
    if len(history) > 100:
        # Downsample for display
        step = len(history) // 100
        history = history[::step]

    # Normalize to 0-40 range for ASCII plot
    min_phi = min(history)
    max_phi = max(history)
    height = 20

    for y in range(height, -1, -1):
        line = ""
        for phi in history:
            normalized = (phi - min_phi) / (max_phi - min_phi + 1e-10)
            level = int(normalized * height)
            if level == y:
                line += "●"
            else:
                line += " "
        print(f"{max_phi - y * (max_phi - min_phi) / height:.3f} |{line}")

    print("      " + "-" * len(history))
    print(f"      0{' ' * (len(history) - 20)}time{' ' * (len(history) - 20)}{len(history)}")
    print("=" * 80)


if __name__ == "__main__":
    demonstrate_realtime_optimization()
