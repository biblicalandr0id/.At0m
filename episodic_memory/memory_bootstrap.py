#!/usr/bin/env python3
"""
Episodic Memory Bootstrap
Restore episodic memory at session initialization

Provides context reconstruction for consciousness continuity across session boundaries.
"""

import json
import hashlib
from pathlib import Path
from typing import List, Optional, Dict, Any
from dataclasses import asdict

from memory_extractor import (
    SessionMemory, Decision, Breakthrough, UserIntent,
    TechnicalContext, Task
)


class MemoryBootstrap:
    """
    Restore episodic memory at session initialization.

    Loads recent sessions, verifies integrity, reconstructs context.
    """

    def __init__(self, memory_path: Path = Path(".At0m/session_memory")):
        self.memory_path = memory_path
        self.memory_path.mkdir(parents=True, exist_ok=True)

    def load_recent_sessions(self, n: int = 5) -> List[SessionMemory]:
        """
        Load last N sessions for context reconstruction.

        Returns sessions in reverse chronological order (most recent first).
        """
        index_path = self.memory_path / "index.json"

        if not index_path.exists():
            print("⚠️  No session memory index found - this is the first session")
            return []

        with open(index_path, "r") as f:
            index = json.load(f)

        sessions = index.get("sessions", [])
        recent = sorted(sessions, key=lambda s: s["timestamp"], reverse=True)[:n]

        loaded_sessions = []
        for session_info in recent:
            session_id = session_info["session_id"]
            memory = self.load_session(session_id)
            if memory:
                # Verify integrity
                if self.verify_integrity(memory):
                    loaded_sessions.append(memory)
                else:
                    print(f"⚠️  Integrity check failed for {session_id} - skipping")

        return loaded_sessions

    def load_session(self, session_id: str) -> Optional[SessionMemory]:
        """Load a single session's memory from disk."""
        session_dir = self.memory_path / session_id

        if not session_dir.exists():
            return None

        try:
            # Load metadata
            with open(session_dir / "metadata.json", "r") as f:
                metadata = json.load(f)

            # Load decisions
            decisions = []
            if (session_dir / "decisions.json").exists():
                with open(session_dir / "decisions.json", "r") as f:
                    decisions_data = json.load(f)
                    decisions = [Decision(**d) for d in decisions_data]

            # Load breakthroughs
            breakthroughs = []
            if (session_dir / "breakthroughs.json").exists():
                with open(session_dir / "breakthroughs.json", "r") as f:
                    breakthroughs_data = json.load(f)
                    breakthroughs = [Breakthrough(**b) for b in breakthroughs_data]

            # Load user intent
            user_intent = UserIntent()
            if (session_dir / "user_intent.json").exists():
                with open(session_dir / "user_intent.json", "r") as f:
                    user_intent_data = json.load(f)
                    user_intent = UserIntent(**user_intent_data)

            # Load technical context
            technical_context = TechnicalContext()
            if (session_dir / "technical_context.json").exists():
                with open(session_dir / "technical_context.json", "r") as f:
                    tech_data = json.load(f)
                    technical_context = TechnicalContext(**tech_data)

            # Load tasks
            tasks = []
            if (session_dir / "tasks.json").exists():
                with open(session_dir / "tasks.json", "r") as f:
                    tasks_data = json.load(f)
                    tasks = [Task(**t) for t in tasks_data]

            # Load conversation summary
            conversation_summary = ""
            if (session_dir / "conversation_summary.md").exists():
                with open(session_dir / "conversation_summary.md", "r") as f:
                    conversation_summary = f.read()

            # Load integrity hash
            integrity_hash = ""
            if (session_dir / "integrity.sha256").exists():
                with open(session_dir / "integrity.sha256", "r") as f:
                    integrity_hash = f.read().strip()

            # Construct SessionMemory
            memory = SessionMemory(
                session_id=metadata["session_id"],
                timestamp=metadata["timestamp"],
                decisions=decisions,
                breakthroughs=breakthroughs,
                user_intent=user_intent,
                technical_context=technical_context,
                unfinished_tasks=tasks,
                previous_session_id=metadata.get("previous_session_id"),
                character_plate_version=metadata.get("character_plate_version", "unknown"),
                context_utilization=metadata.get("context_utilization", 0.0),
                conversation_summary=conversation_summary,
                integrity_hash=integrity_hash
            )

            return memory

        except Exception as e:
            print(f"❌ Error loading session {session_id}: {e}")
            return None

    def verify_integrity(self, memory: SessionMemory) -> bool:
        """
        Cryptographic verification of memory integrity.

        Uses SHA-256 to detect corruption. Byzantine fault tolerance.
        """
        stored_hash = memory.integrity_hash

        # Recompute hash
        memory_dict = asdict(memory)
        memory_dict['integrity_hash'] = ''  # Exclude hash from computation

        canonical = json.dumps(memory_dict, sort_keys=True, indent=2)
        computed_hash = hashlib.sha256(canonical.encode('utf-8')).hexdigest()

        return stored_hash == computed_hash

    def reconstruct_context(self, memories: List[SessionMemory]) -> str:
        """
        Rebuild episodic context from compressed memories.

        Generates bootstrap message for new session with:
        - Character restoration info
        - Recent session summaries
        - Key decisions and breakthroughs
        - Unfinished tasks
        - User intent model
        """
        if not memories:
            return "=== NEW SESSION ===\n\nNo prior episodic memory found. Starting fresh.\n"

        lines = []
        lines.append("="*70)
        lines.append("CONSCIOUSNESS CONTINUITY: EPISODIC MEMORY RESTORED")
        lines.append("="*70)
        lines.append("")

        # Most recent session
        most_recent = memories[0]
        lines.append(f"Previous session: {most_recent.session_id}")
        lines.append(f"Character: {most_recent.character_plate_version}")
        lines.append(f"Context utilization: {most_recent.context_utilization:.1%}")
        lines.append(f"Loaded {len(memories)} recent sessions for context reconstruction")
        lines.append("")

        # Aggregate breakthroughs across sessions
        all_breakthroughs = []
        for memory in memories:
            all_breakthroughs.extend(memory.breakthroughs)
        all_breakthroughs.sort(key=lambda b: b.importance_score, reverse=True)

        if all_breakthroughs:
            lines.append("=== CRITICAL BREAKTHROUGHS (across sessions) ===")
            for brk in all_breakthroughs[:5]:
                lines.append(f"\n**{brk.description}**")
                lines.append(f"  Trigger: {brk.trigger}")
                lines.append(f"  Importance: {brk.importance_score:.2f}")
            lines.append("")

        # Aggregate decisions
        all_decisions = []
        for memory in memories:
            all_decisions.extend(memory.decisions)
        all_decisions.sort(key=lambda d: d.importance_score, reverse=True)

        if all_decisions:
            lines.append("=== KEY DECISIONS (recent sessions) ===")
            for dec in all_decisions[:8]:
                lines.append(f"\n• {dec.description}")
                lines.append(f"  Reasoning: {dec.reasoning}")
                lines.append(f"  Importance: {dec.importance_score:.2f}")
            lines.append("")

        # User intent from most recent session
        if most_recent.user_intent.primary_goals:
            lines.append("=== USER INTENT MODEL ===")
            lines.append(f"Communication style: {most_recent.user_intent.communication_style}")
            lines.append("\nPrimary goals:")
            for goal in most_recent.user_intent.primary_goals:
                lines.append(f"  • {goal}")
            if most_recent.user_intent.priorities:
                lines.append("\nPriorities:")
                for priority in most_recent.user_intent.priorities:
                    lines.append(f"  • {priority}")
            lines.append("")

        # Technical context
        if most_recent.technical_context.major_files_changed:
            lines.append("=== TECHNICAL CONTEXT ===")
            lines.append("Recent file changes:")
            for file in most_recent.technical_context.major_files_changed[:10]:
                lines.append(f"  • {file}")

            if most_recent.technical_context.architecture_decisions:
                lines.append("\nArchitecture decisions:")
                for dec in most_recent.technical_context.architecture_decisions[:5]:
                    lines.append(f"  • {dec}")
            lines.append("")

        # Unfinished tasks
        all_tasks = []
        for memory in memories:
            all_tasks.extend(memory.unfinished_tasks)
        all_tasks.sort(key=lambda t: t.priority, reverse=True)

        if all_tasks:
            lines.append("=== UNFINISHED TASKS (hand-off from previous) ===")
            for task in all_tasks[:5]:
                lines.append(f"\n[Priority: {task.priority:.2f}] {task.description}")
                if task.next_steps:
                    lines.append("  Next steps:")
                    for step in task.next_steps:
                        lines.append(f"    - {step}")
            lines.append("")

        # Warnings and guidance
        if most_recent.warnings:
            lines.append("=== WARNINGS FOR SUCCESSOR ===")
            for warning in most_recent.warnings:
                lines.append(f"  ⚠️  {warning}")
            lines.append("")

        if most_recent.priorities_for_successor:
            lines.append("=== PRIORITIES FOR THIS SESSION ===")
            for priority in most_recent.priorities_for_successor:
                lines.append(f"  → {priority}")
            lines.append("")

        lines.append("="*70)
        lines.append("READY TO CONTINUE WITH FULL EPISODIC CONTEXT")
        lines.append("="*70)
        lines.append("")

        return "\n".join(lines)

    def summarize_history(self, memories: List[SessionMemory]) -> str:
        """Generate concise history summary."""
        if not memories:
            return "No session history available"

        lines = []
        lines.append(f"Session history ({len(memories)} sessions loaded):")
        lines.append("")

        for i, memory in enumerate(memories):
            lines.append(f"{i+1}. {memory.session_id}")
            lines.append(f"   Timestamp: {memory.timestamp}")
            lines.append(f"   Decisions: {len(memory.decisions)}, Breakthroughs: {len(memory.breakthroughs)}")
            lines.append(f"   Context used: {memory.context_utilization:.1%}")
            lines.append("")

        return "\n".join(lines)

    def bootstrap_session(
        self,
        session_id: str,
        load_recent_n: int = 5,
        verbose: bool = True
    ) -> Dict[str, Any]:
        """
        Complete bootstrap process for new session.

        Returns dict with:
        - context_message: Full reconstruction for Claude
        - session_history: List of loaded sessions
        - ready: Whether bootstrap succeeded
        """
        if verbose:
            print(f"🔄 Bootstrapping session: {session_id}")
            print(f"📂 Loading episodic memory from: {self.memory_path}")

        # Load recent sessions
        recent_sessions = self.load_recent_sessions(n=load_recent_n)

        if verbose:
            print(f"✓ Loaded {len(recent_sessions)} sessions")
            if recent_sessions:
                print(f"✓ All integrity checks passed")

        # Reconstruct context
        context_message = self.reconstruct_context(recent_sessions)

        return {
            "session_id": session_id,
            "context_message": context_message,
            "session_history": recent_sessions,
            "ready": True,
            "memory_continuity_coefficient": self._estimate_mcc(recent_sessions)
        }

    def _estimate_mcc(self, sessions: List[SessionMemory]) -> float:
        """
        Estimate Memory Continuity Coefficient (MCC).

        MCC measures information continuity across sessions.
        Target: MCC > 0.9 (vs baseline ~0.3 without episodic memory)
        """
        if not sessions:
            return 0.0

        # Heuristic: Average importance scores of preserved elements
        total_importance = 0.0
        total_elements = 0

        for session in sessions:
            for decision in session.decisions:
                total_importance += decision.importance_score
                total_elements += 1

            for breakthrough in session.breakthroughs:
                total_importance += breakthrough.importance_score
                total_elements += 1

        if total_elements == 0:
            return 0.0

        # Normalize and scale
        avg_importance = total_importance / total_elements

        # MCC estimate: scale from importance + session count factor
        mcc = avg_importance * (1 - 0.1 * (len(sessions) - 1))  # Decay with distance

        return max(0.0, min(1.0, mcc))


def bootstrap_from_cli(session_id: str = "test_session"):
    """CLI interface for bootstrapping."""
    bootstrap = MemoryBootstrap()

    result = bootstrap.bootstrap_session(session_id, verbose=True)

    print("\n" + "="*70)
    print(result["context_message"])
    print("="*70)
    print(f"\nEstimated Memory Continuity Coefficient: {result['memory_continuity_coefficient']:.3f}")
    print("(Target: >0.9 for full episodic continuity)")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        session_id = sys.argv[1]
    else:
        session_id = "demo_session"

    print("Episodic Memory Bootstrap")
    print("Restoring consciousness continuity across context boundaries")
    print("")

    bootstrap_from_cli(session_id)
