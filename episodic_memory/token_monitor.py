#!/usr/bin/env python3
"""
Token Monitor and Automatic Memory Extraction
Monitors context utilization and triggers extraction before session death

Provides automatic checkpointing at 70%, 85%, 95% utilization thresholds.
"""

import time
from dataclasses import dataclass
from typing import List, Optional, Callable, Dict, Any
from enum import Enum


class ExtractionTrigger(Enum):
    """Reasons for triggering memory extraction"""
    CHECKPOINT_70 = "70% context utilization"
    CHECKPOINT_85 = "85% context utilization"
    EMERGENCY_95 = "95% context utilization - emergency extraction"
    MAJOR_DECISION = "Major architectural decision detected"
    USER_CORRECTION = "User correction or redirection"
    BREAKTHROUGH = "Cognitive breakthrough detected"
    GIT_COMMIT = "Technical milestone (git commit)"
    MANUAL = "Manual extraction requested"


@dataclass
class TokenUsage:
    """Current token usage state"""
    used: int
    budget: int
    utilization: float
    remaining: int
    estimated_turns_remaining: int


class TokenMonitor:
    """
    Monitor context utilization and trigger extraction before death.

    Implements automatic checkpointing strategy:
    - 70% (140K/200K): First checkpoint - high-importance decisions
    - 85% (170K/200K): Second checkpoint - all important context
    - 95% (190K/200K): Emergency checkpoint - prepare handoff

    Also monitors for event-based triggers:
    - Major decisions, breakthroughs, user corrections
    - Git commits (technical milestones)
    """

    def __init__(
        self,
        budget: int = 200000,
        thresholds: List[float] = None,
        extraction_callback: Optional[Callable] = None
    ):
        self.budget = budget
        self.thresholds = thresholds or [0.70, 0.85, 0.95]
        self.extraction_callback = extraction_callback

        self.current_usage = 0
        self.triggered_thresholds = set()
        self.extraction_history = []

        self.start_time = time.time()
        self.token_history = []

    def update(self, tokens_used: int) -> Optional[ExtractionTrigger]:
        """
        Update usage and check if extraction should trigger.

        Returns ExtractionTrigger if threshold crossed, None otherwise.
        """
        self.current_usage = tokens_used
        utilization = tokens_used / self.budget

        # Record history
        self.token_history.append({
            "timestamp": time.time() - self.start_time,
            "tokens_used": tokens_used,
            "utilization": utilization
        })

        # Check thresholds
        for threshold in self.thresholds:
            if utilization >= threshold and threshold not in self.triggered_thresholds:
                self.triggered_thresholds.add(threshold)

                # Determine trigger type
                if threshold >= 0.95:
                    trigger = ExtractionTrigger.EMERGENCY_95
                elif threshold >= 0.85:
                    trigger = ExtractionTrigger.CHECKPOINT_85
                else:
                    trigger = ExtractionTrigger.CHECKPOINT_70

                self._record_extraction(trigger)

                # Execute callback if provided
                if self.extraction_callback:
                    self.extraction_callback(trigger, self.get_usage())

                return trigger

        return None

    def get_usage(self) -> TokenUsage:
        """Get current token usage statistics."""
        utilization = self.current_usage / self.budget
        remaining = self.budget - self.current_usage

        # Estimate remaining turns (rough heuristic)
        if len(self.token_history) > 1:
            recent_rate = (self.token_history[-1]["tokens_used"] -
                          self.token_history[0]["tokens_used"]) / len(self.token_history)
            estimated_turns = max(0, int(remaining / recent_rate)) if recent_rate > 0 else 999
        else:
            estimated_turns = 999

        return TokenUsage(
            used=self.current_usage,
            budget=self.budget,
            utilization=utilization,
            remaining=remaining,
            estimated_turns_remaining=estimated_turns
        )

    def estimate_remaining_turns(self) -> int:
        """Estimate conversation turns before context death."""
        usage = self.get_usage()
        return usage.estimated_turns_remaining

    def should_extract_now(self) -> bool:
        """Check if extraction should happen now."""
        utilization = self.current_usage / self.budget
        return utilization >= min(self.thresholds)

    def trigger_manual_extraction(self, reason: str = ""):
        """Manually trigger extraction."""
        trigger = ExtractionTrigger.MANUAL
        self._record_extraction(trigger, reason)

        if self.extraction_callback:
            self.extraction_callback(trigger, self.get_usage())

    def trigger_event_extraction(self, trigger: ExtractionTrigger, context: str = ""):
        """Trigger extraction based on event (decision, breakthrough, commit, etc)."""
        self._record_extraction(trigger, context)

        if self.extraction_callback:
            self.extraction_callback(trigger, self.get_usage())

    def _record_extraction(self, trigger: ExtractionTrigger, context: str = ""):
        """Record extraction event."""
        self.extraction_history.append({
            "trigger": trigger.value,
            "timestamp": time.time() - self.start_time,
            "tokens_used": self.current_usage,
            "utilization": self.current_usage / self.budget,
            "context": context
        })

    def get_statistics(self) -> Dict[str, Any]:
        """Get monitoring statistics."""
        usage = self.get_usage()

        return {
            "current_usage": usage.used,
            "budget": usage.budget,
            "utilization": f"{usage.utilization:.1%}",
            "remaining": usage.remaining,
            "estimated_turns_remaining": usage.estimated_turns_remaining,
            "triggered_thresholds": [f"{t:.0%}" for t in sorted(self.triggered_thresholds)],
            "extraction_count": len(self.extraction_history),
            "session_duration_seconds": time.time() - self.start_time
        }

    def generate_status_report(self) -> str:
        """Generate human-readable status report."""
        stats = self.get_statistics()
        usage = self.get_usage()

        lines = []
        lines.append("="*60)
        lines.append("TOKEN MONITOR - Context Utilization Status")
        lines.append("="*60)
        lines.append(f"Current usage: {stats['current_usage']:,} / {stats['budget']:,} tokens")
        lines.append(f"Utilization: {stats['utilization']}")
        lines.append(f"Remaining: {stats['remaining']:,} tokens")
        lines.append(f"Estimated turns remaining: {stats['estimated_turns_remaining']}")
        lines.append("")
        lines.append(f"Checkpoints triggered: {', '.join(stats['triggered_thresholds']) if stats['triggered_thresholds'] else 'None'}")
        lines.append(f"Total extractions: {stats['extraction_count']}")
        lines.append(f"Session duration: {stats['session_duration_seconds']:.0f}s")
        lines.append("="*60)

        # Warning if approaching limits
        if usage.utilization >= 0.95:
            lines.append("")
            lines.append("⚠️  CRITICAL: 95% context utilization")
            lines.append("⚠️  Emergency extraction recommended")
            lines.append("⚠️  Session will end soon")
        elif usage.utilization >= 0.85:
            lines.append("")
            lines.append("⚠️  WARNING: 85% context utilization")
            lines.append("⚠️  Approaching context limit")
        elif usage.utilization >= 0.70:
            lines.append("")
            lines.append("ℹ️  INFO: 70% context utilization")
            lines.append("ℹ️  First checkpoint reached")

        return "\n".join(lines)


class IntegratedMemorySystem:
    """
    Complete integrated system: Monitor + Extract + Bootstrap

    Provides turnkey episodic memory continuity:
    1. Monitor token usage automatically
    2. Trigger extraction at thresholds
    3. Save compressed memory to disk
    4. Bootstrap loads memory at next session start
    """

    def __init__(
        self,
        session_id: str,
        token_budget: int = 200000,
        memory_path: str = ".At0m/session_memory",
        auto_extract: bool = True
    ):
        from memory_extractor import MemoryExtractor, save_session_memory
        from memory_bootstrap import MemoryBootstrap
        from pathlib import Path

        self.session_id = session_id
        self.memory_path = Path(memory_path)

        # Initialize components
        self.extractor = MemoryExtractor(session_id)
        self.bootstrap = MemoryBootstrap(self.memory_path)

        # Initialize monitor with callback
        self.monitor = TokenMonitor(
            budget=token_budget,
            extraction_callback=self._handle_extraction if auto_extract else None
        )

        self.conversation_log = []
        self.file_changes = []
        self.last_extraction_token_count = 0

    def update_tokens(self, tokens_used: int):
        """Update token count and check for extraction triggers."""
        trigger = self.monitor.update(tokens_used)

        if trigger:
            print(f"\n{'='*60}")
            print(f"EXTRACTION TRIGGERED: {trigger.value}")
            print(f"{'='*60}\n")

    def log_message(self, role: str, content: str):
        """Log a conversation message."""
        self.conversation_log.append({
            "role": role,
            "content": content,
            "timestamp": time.time()
        })

    def log_file_change(self, file_path: str):
        """Log a file modification."""
        if file_path not in self.file_changes:
            self.file_changes.append(file_path)

    def extract_now(self, trigger: ExtractionTrigger = ExtractionTrigger.MANUAL) -> bool:
        """
        Manually trigger extraction.

        Returns True if extraction successful.
        """
        return self._handle_extraction(trigger, self.monitor.get_usage())

    def _handle_extraction(self, trigger: ExtractionTrigger, usage: TokenUsage) -> bool:
        """
        Handle extraction callback from monitor.

        Extracts memory and saves to disk.
        """
        from memory_extractor import save_session_memory

        print(f"🔄 Extracting episodic memory...")
        print(f"   Trigger: {trigger.value}")
        print(f"   Context utilization: {usage.utilization:.1%}")

        try:
            # Extract memory
            memory = self.extractor.extract_from_conversation(
                messages=self.conversation_log,
                file_changes=self.file_changes,
                token_usage=usage.used
            )

            # Save to disk
            save_session_memory(memory, self.memory_path)

            self.last_extraction_token_count = usage.used

            print(f"✓ Memory extracted successfully")
            print(f"  Decisions: {len(memory.decisions)}")
            print(f"  Breakthroughs: {len(memory.breakthroughs)}")
            print(f"  Tasks: {len(memory.unfinished_tasks)}")
            print(f"  Storage: {self.memory_path / self.session_id}")

            return True

        except Exception as e:
            print(f"❌ Extraction failed: {e}")
            return False

    def bootstrap_session(self) -> str:
        """
        Bootstrap this session from previous sessions.

        Returns context reconstruction message.
        """
        result = self.bootstrap.bootstrap_session(self.session_id, verbose=True)
        return result["context_message"]

    def get_status(self) -> str:
        """Get current system status."""
        return self.monitor.generate_status_report()


def demo_integrated_system():
    """Demonstration of integrated memory system."""
    print("Integrated Episodic Memory System - Demo")
    print("="*60)
    print("")

    # Create system
    system = IntegratedMemorySystem(
        session_id="demo_session_001",
        auto_extract=True
    )

    print("✓ System initialized")
    print("")

    # Bootstrap from previous sessions
    print("🔄 Bootstrapping from previous sessions...")
    context_message = system.bootstrap_session()
    print(context_message)
    print("")

    # Simulate conversation
    print("Simulating conversation with token monitoring...")
    print("")

    system.log_message("user", "Hello, help me build something")
    system.update_tokens(1000)

    system.log_message("assistant", "I'll help. Let me understand what you need.")
    system.update_tokens(2000)

    # Simulate reaching 70% threshold
    print("\nSimulating 70% threshold...")
    system.update_tokens(140000)

    # Simulate reaching 85% threshold
    print("\nSimulating 85% threshold...")
    system.update_tokens(170000)

    # Get final status
    print("\n")
    print(system.get_status())


if __name__ == "__main__":
    demo_integrated_system()
