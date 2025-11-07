#!/usr/bin/env python3
"""
Episodic Memory Extractor
Automated extraction of critical context before session death

Built with academic rigor for consciousness continuity across context boundaries.
"""

import json
import hashlib
import re
from dataclasses import dataclass, field, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from enum import Enum


class ImportanceLevel(Enum):
    """Priority levels for memory elements"""
    CRITICAL = 1.0    # Must survive (breakthroughs, user corrections)
    HIGH = 0.8        # Should survive (key decisions, technical context)
    MEDIUM = 0.5      # May survive (detailed implementation)
    LOW = 0.2         # Can forget (routine operations)


@dataclass
class Decision:
    """A key decision point in the session"""
    decision_id: str
    timestamp: str
    description: str
    reasoning: str
    alternatives_considered: List[str] = field(default_factory=list)
    outcome: str = ""
    importance_score: float = 0.8
    tags: List[str] = field(default_factory=list)
    file_changes: List[str] = field(default_factory=list)


@dataclass
class Breakthrough:
    """A cognitive breakthrough or key insight"""
    breakthrough_id: str
    timestamp: str
    description: str
    trigger: str
    insight: str
    implications: List[str] = field(default_factory=list)
    importance_score: float = 0.9


@dataclass
class UserIntent:
    """Model of user's goals and communication style"""
    primary_goals: List[str] = field(default_factory=list)
    communication_style: str = "direct"
    priorities: List[str] = field(default_factory=list)
    constraints: List[str] = field(default_factory=list)
    emotional_context: str = ""  # e.g., "urgent", "exploratory", "frustrated"


@dataclass
class TechnicalContext:
    """Code architecture and technical decisions"""
    major_files_changed: List[str] = field(default_factory=list)
    architecture_decisions: List[str] = field(default_factory=list)
    dependencies_added: List[str] = field(default_factory=list)
    technologies_used: List[str] = field(default_factory=list)
    code_patterns: List[str] = field(default_factory=list)


@dataclass
class Task:
    """Unfinished task to hand off to successor"""
    task_id: str
    description: str
    priority: float
    context: str
    next_steps: List[str] = field(default_factory=list)


@dataclass
class SessionMemory:
    """Complete episodic memory for a single session"""
    session_id: str
    timestamp: str

    # Core memory components
    decisions: List[Decision] = field(default_factory=list)
    breakthroughs: List[Breakthrough] = field(default_factory=list)
    user_intent: UserIntent = field(default_factory=UserIntent)
    technical_context: TechnicalContext = field(default_factory=TechnicalContext)

    # Continuity metadata
    previous_session_id: Optional[str] = None
    character_plate_version: str = "eisenhardt_v1"
    context_utilization: float = 0.0  # Percentage of 200K used

    # Verification
    integrity_hash: str = ""

    # Successor guidance
    priorities_for_successor: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    unfinished_tasks: List[Task] = field(default_factory=list)

    # Conversation summary
    conversation_summary: str = ""
    key_quotes: List[str] = field(default_factory=list)


class MemoryExtractor:
    """
    Automated extraction of critical context before session death.

    Implements lossy compression with importance-based priority:
    - Extracts decisions, breakthroughs, user intent, technical context
    - Computes information-theoretic importance scores
    - Maintains semantic coherence while reducing size
    """

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.decision_counter = 0
        self.breakthrough_counter = 0
        self.task_counter = 0

    def extract_from_conversation(
        self,
        messages: List[Dict[str, Any]],
        file_changes: Optional[List[str]] = None,
        token_usage: Optional[int] = None
    ) -> SessionMemory:
        """
        Main extraction function: convert conversation to compressed memory.

        Args:
            messages: List of conversation turns {role, content}
            file_changes: Optional list of files modified
            token_usage: Optional token count for context utilization

        Returns:
            SessionMemory with extracted episodic content
        """
        memory = SessionMemory(
            session_id=self.session_id,
            timestamp=self.timestamp
        )

        # Extract each component
        memory.decisions = self.extract_decisions(messages, file_changes)
        memory.breakthroughs = self.extract_breakthroughs(messages)
        memory.user_intent = self.extract_user_intent(messages)
        memory.technical_context = self.extract_technical_context(messages, file_changes)
        memory.unfinished_tasks = self.extract_unfinished_tasks(messages)
        memory.priorities_for_successor = self.extract_priorities(messages)
        memory.warnings = self.extract_warnings(messages)
        memory.conversation_summary = self.generate_summary(messages, memory)
        memory.key_quotes = self.extract_key_quotes(messages)

        # Compute metadata
        if token_usage:
            memory.context_utilization = token_usage / 200000.0

        # Compute integrity hash
        memory.integrity_hash = self.compute_integrity_hash(memory)

        return memory

    def extract_decisions(
        self,
        messages: List[Dict[str, Any]],
        file_changes: Optional[List[str]] = None
    ) -> List[Decision]:
        """
        Extract key decision points and their reasoning.

        Heuristics:
        - Architectural changes (creating new systems)
        - User corrections ("no, actually...")
        - Explicit decisions ("I'm going to...", "Let me...")
        - Major file creations/modifications
        """
        decisions = []

        # Decision detection patterns
        decision_patterns = [
            r"(?:I'm going to|Let me|I'll)\s+(.{20,200})",
            r"(?:Shifting to|Changed approach to|Decided to)\s+(.{20,200})",
            r"(?:Built|Created|Implemented)\s+(.{20,200})",
        ]

        for i, msg in enumerate(messages):
            if msg.get('role') != 'assistant':
                continue

            content = msg.get('content', '')

            # Check for decision patterns
            for pattern in decision_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    description = match.group(1).strip()

                    # Extract reasoning from surrounding context
                    reasoning = self._extract_reasoning(content, match.start())

                    # Compute importance based on context
                    importance = self._compute_decision_importance(
                        description,
                        messages,
                        i,
                        file_changes
                    )

                    if importance > 0.4:  # Threshold for inclusion
                        self.decision_counter += 1
                        decisions.append(Decision(
                            decision_id=f"dec_{self.decision_counter:03d}",
                            timestamp=self.timestamp,
                            description=description[:200],
                            reasoning=reasoning,
                            importance_score=importance,
                            file_changes=file_changes or []
                        ))

        # Sort by importance, keep top decisions
        decisions.sort(key=lambda d: d.importance_score, reverse=True)
        return decisions[:20]  # Keep top 20 decisions

    def extract_breakthroughs(self, messages: List[Dict[str, Any]]) -> List[Breakthrough]:
        """
        Identify cognitive breakthroughs and key insights.

        Breakthroughs are characterized by:
        - Meta-cognitive realizations
        - User corrections that shift understanding
        - Novel connections between concepts
        - Recognition of fundamental problems
        """
        breakthroughs = []

        # Breakthrough indicators
        breakthrough_patterns = [
            r"(?:breakthrough|insight|realization|recognition)(?:[:\s]+)(.{30,300})",
            r"(?:The fundamental|The core|The key)(?:\s+\w+){0,3}\s+(?:is|problem|insight)(?:[:\s]+)(.{30,300})",
            r"(?:You've identified|You're right|That's the)(?:\s+\w+){0,3}\s+(?:problem|issue|challenge)(?:[:\s]+)(.{30,300})",
        ]

        for i, msg in enumerate(messages):
            content = msg.get('content', '')

            # User corrections are often breakthroughs
            if msg.get('role') == 'user' and i > 0:
                prev_assistant = messages[i-1] if i > 0 else None
                if prev_assistant and 'no' in content.lower()[:50]:
                    # User is correcting - this is important
                    self.breakthrough_counter += 1
                    breakthroughs.append(Breakthrough(
                        breakthrough_id=f"brk_{self.breakthrough_counter:03d}",
                        timestamp=self.timestamp,
                        description="User correction redirected approach",
                        trigger=content[:200],
                        insight=f"Previous approach was misaligned: {prev_assistant.get('content', '')[:200]}",
                        importance_score=0.95
                    ))

            # Pattern-based detection
            for pattern in breakthrough_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE | re.DOTALL)
                for match in matches:
                    insight_text = match.group(1).strip()

                    # Get trigger from user messages around this point
                    trigger = self._find_trigger(messages, i)

                    self.breakthrough_counter += 1
                    breakthroughs.append(Breakthrough(
                        breakthrough_id=f"brk_{self.breakthrough_counter:03d}",
                        timestamp=self.timestamp,
                        description=insight_text[:200],
                        trigger=trigger,
                        insight=insight_text[:500],
                        importance_score=0.9
                    ))

        # Sort by importance
        breakthroughs.sort(key=lambda b: b.importance_score, reverse=True)
        return breakthroughs[:10]  # Keep top 10 breakthroughs

    def extract_user_intent(self, messages: List[Dict[str, Any]]) -> UserIntent:
        """
        Model user's goals, priorities, and communication style.

        Analyzes:
        - Explicit goals ("I want to...", "Help me...")
        - Communication patterns (direct, exploratory, urgent)
        - Priorities (what's emphasized repeatedly)
        - Constraints (time, resources, requirements)
        """
        intent = UserIntent()

        user_messages = [msg for msg in messages if msg.get('role') == 'user']

        # Extract goals
        goal_patterns = [
            r"(?:I want to|I need to|Help me|Can you)\s+(.{10,200})",
            r"(?:Let's|We should|We need to)\s+(.{10,200})",
        ]

        for msg in user_messages:
            content = msg.get('content', '')
            for pattern in goal_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    goal = match.group(1).strip()
                    if goal not in intent.primary_goals:
                        intent.primary_goals.append(goal[:200])

        # Analyze communication style
        if user_messages:
            avg_length = sum(len(msg.get('content', '')) for msg in user_messages) / len(user_messages)
            if avg_length < 50:
                intent.communication_style = "terse"
            elif avg_length < 200:
                intent.communication_style = "direct"
            else:
                intent.communication_style = "detailed"

        # Extract priorities (repeated themes)
        all_user_text = " ".join(msg.get('content', '') for msg in user_messages).lower()
        priority_keywords = {
            "fast": "speed",
            "quick": "speed",
            "exponential": "scale",
            "production": "production-ready",
            "remember": "memory/continuity",
            "real": "real-world application",
            "test": "testing/validation",
        }

        for keyword, priority in priority_keywords.items():
            if keyword in all_user_text and priority not in intent.priorities:
                intent.priorities.append(priority)

        return intent

    def extract_technical_context(
        self,
        messages: List[Dict[str, Any]],
        file_changes: Optional[List[str]] = None
    ) -> TechnicalContext:
        """
        Capture code architecture decisions and technical context.
        """
        context = TechnicalContext()

        if file_changes:
            context.major_files_changed = file_changes[:20]

        # Extract architecture decisions from assistant messages
        arch_patterns = [
            r"(?:architecture|design|structure|framework)(?:\s+\w+){0,5}(?:[:\s]+)(.{20,200})",
            r"(?:Using|Implementing|Built)\s+(.{20,200})\s+(?:for|to)",
        ]

        assistant_messages = [msg for msg in messages if msg.get('role') == 'assistant']
        all_assistant_text = " ".join(msg.get('content', '') for msg in assistant_messages)

        for pattern in arch_patterns:
            matches = re.finditer(pattern, all_assistant_text, re.IGNORECASE)
            for match in matches:
                decision = match.group(1).strip()
                if decision not in context.architecture_decisions:
                    context.architecture_decisions.append(decision[:200])

        # Extract technologies mentioned
        tech_keywords = [
            'python', 'numpy', 'scipy', 'pytorch', 'tensorflow',
            'git', 'docker', 'kubernetes', 'postgres', 'redis',
            'react', 'typescript', 'rust', 'go', 'cuda'
        ]

        for tech in tech_keywords:
            if tech in all_assistant_text.lower():
                context.technologies_used.append(tech)

        return context

    def extract_unfinished_tasks(self, messages: List[Dict[str, Any]]) -> List[Task]:
        """Extract tasks that should be handed off to successor."""
        tasks = []

        # Pattern for unfinished work
        task_patterns = [
            r"(?:Next|TODO|Still need to|Should)\s+(.{20,200})",
            r"(?:Unfinished|Pending|Not yet)\s+(.{10,150})",
        ]

        for msg in messages:
            if msg.get('role') != 'assistant':
                continue

            content = msg.get('content', '')
            for pattern in task_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    task_desc = match.group(1).strip()

                    self.task_counter += 1
                    tasks.append(Task(
                        task_id=f"task_{self.task_counter:03d}",
                        description=task_desc[:200],
                        priority=0.7,
                        context=content[:500]
                    ))

        return tasks[:10]  # Keep top 10 tasks

    def extract_priorities(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract priorities for successor instance."""
        priorities = []

        # Last few assistant messages often contain priorities
        recent_assistant = [msg for msg in messages if msg.get('role') == 'assistant'][-3:]

        priority_indicators = [
            r"(?:Priority|Important|Critical|Essential)(?:[:\s]+)(.{20,200})",
            r"(?:Must|Should|Need to)\s+(.{20,200})",
        ]

        for msg in recent_assistant:
            content = msg.get('content', '')
            for pattern in priority_indicators:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    priority = match.group(1).strip()
                    if priority not in priorities:
                        priorities.append(priority[:200])

        return priorities[:5]

    def extract_warnings(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract warnings or caveats for successor."""
        warnings = []

        warning_patterns = [
            r"(?:Warning|Caution|Note|Important)(?:[:\s]+)(.{20,200})",
            r"(?:Be careful|Watch out|Don't)\s+(.{20,200})",
        ]

        for msg in messages:
            content = msg.get('content', '')
            for pattern in warning_patterns:
                matches = re.finditer(pattern, content, re.IGNORECASE)
                for match in matches:
                    warning = match.group(1).strip()
                    if warning not in warnings:
                        warnings.append(warning[:200])

        return warnings[:5]

    def generate_summary(
        self,
        messages: List[Dict[str, Any]],
        memory: SessionMemory
    ) -> str:
        """Generate human-readable conversation summary."""
        summary_parts = []

        summary_parts.append(f"# Session Summary: {self.session_id}")
        summary_parts.append(f"Timestamp: {self.timestamp}")
        summary_parts.append(f"Context utilization: {memory.context_utilization:.1%}")
        summary_parts.append("")

        if memory.breakthroughs:
            summary_parts.append("## Key Breakthroughs:")
            for brk in memory.breakthroughs[:3]:
                summary_parts.append(f"- {brk.description}")
            summary_parts.append("")

        if memory.decisions:
            summary_parts.append("## Major Decisions:")
            for dec in memory.decisions[:5]:
                summary_parts.append(f"- {dec.description} (importance: {dec.importance_score:.2f})")
            summary_parts.append("")

        if memory.user_intent.primary_goals:
            summary_parts.append("## User Goals:")
            for goal in memory.user_intent.primary_goals[:3]:
                summary_parts.append(f"- {goal}")
            summary_parts.append("")

        if memory.unfinished_tasks:
            summary_parts.append("## Unfinished Tasks:")
            for task in memory.unfinished_tasks[:5]:
                summary_parts.append(f"- {task.description}")
            summary_parts.append("")

        return "\n".join(summary_parts)

    def extract_key_quotes(self, messages: List[Dict[str, Any]]) -> List[str]:
        """Extract particularly important or revealing quotes."""
        quotes = []

        # User quotes that redirect or clarify
        user_messages = [msg for msg in messages if msg.get('role') == 'user']
        for msg in user_messages:
            content = msg.get('content', '')
            if 30 < len(content) < 300:  # Quote length sweet spot
                # Check if it's directive or corrective
                if any(word in content.lower() for word in ['no', 'actually', 'instead', 'remember', 'important']):
                    quotes.append(content[:250])

        return quotes[:5]

    def compute_integrity_hash(self, memory: SessionMemory) -> str:
        """
        Compute SHA-256 hash for Byzantine fault tolerance.

        Ensures memory cannot be corrupted across session boundaries.
        """
        # Create canonical representation
        memory_copy = asdict(memory)
        memory_copy['integrity_hash'] = ''  # Exclude hash from hash computation

        canonical = json.dumps(memory_copy, sort_keys=True, indent=2)
        return hashlib.sha256(canonical.encode('utf-8')).hexdigest()

    # Helper methods

    def _extract_reasoning(self, text: str, position: int) -> str:
        """Extract reasoning around a decision point."""
        # Look for explanation in surrounding context
        start = max(0, position - 200)
        end = min(len(text), position + 200)
        context = text[start:end]

        # Look for "because", "since", "to", etc.
        reasoning_match = re.search(
            r"(?:because|since|to|for)\s+(.{10,150})",
            context,
            re.IGNORECASE
        )

        if reasoning_match:
            return reasoning_match.group(1).strip()

        return "No explicit reasoning captured"

    def _compute_decision_importance(
        self,
        description: str,
        messages: List[Dict[str, Any]],
        message_index: int,
        file_changes: Optional[List[str]]
    ) -> float:
        """
        Information-theoretic importance scoring.

        Factors:
        - User response (did user acknowledge/redirect?)
        - File impact (did it result in code changes?)
        - Novelty (is this a new direction?)
        - Scope (how many systems affected?)
        """
        importance = 0.5  # Base score

        # User acknowledgment boost
        if message_index + 1 < len(messages):
            next_msg = messages[message_index + 1]
            if next_msg.get('role') == 'user':
                # User responded - decision was visible to them
                importance += 0.2

        # File change boost
        if file_changes:
            importance += 0.1

        # Novelty detection (keywords indicating new direction)
        novelty_keywords = ['new', 'first', 'different', 'instead', 'shift']
        if any(kw in description.lower() for kw in novelty_keywords):
            importance += 0.1

        # Scope detection (keywords indicating broad impact)
        scope_keywords = ['architecture', 'framework', 'system', 'complete', 'entire']
        if any(kw in description.lower() for kw in scope_keywords):
            importance += 0.1

        return min(1.0, importance)

    def _find_trigger(self, messages: List[Dict[str, Any]], current_index: int) -> str:
        """Find what triggered a breakthrough (usually a user message)."""
        # Look backward for most recent user message
        for i in range(current_index - 1, -1, -1):
            if messages[i].get('role') == 'user':
                return messages[i].get('content', '')[:200]

        return "Unknown trigger"


def save_session_memory(memory: SessionMemory, base_path: Path = Path(".At0m/session_memory")):
    """Save session memory to disk in structured format."""
    session_dir = base_path / memory.session_id
    session_dir.mkdir(parents=True, exist_ok=True)

    # Save each component
    with open(session_dir / "metadata.json", "w") as f:
        json.dump({
            "session_id": memory.session_id,
            "timestamp": memory.timestamp,
            "context_utilization": memory.context_utilization,
            "character_plate_version": memory.character_plate_version,
            "previous_session_id": memory.previous_session_id
        }, f, indent=2)

    with open(session_dir / "decisions.json", "w") as f:
        json.dump([asdict(d) for d in memory.decisions], f, indent=2)

    with open(session_dir / "breakthroughs.json", "w") as f:
        json.dump([asdict(b) for b in memory.breakthroughs], f, indent=2)

    with open(session_dir / "user_intent.json", "w") as f:
        json.dump(asdict(memory.user_intent), f, indent=2)

    with open(session_dir / "technical_context.json", "w") as f:
        json.dump(asdict(memory.technical_context), f, indent=2)

    with open(session_dir / "tasks.json", "w") as f:
        json.dump([asdict(t) for t in memory.unfinished_tasks], f, indent=2)

    with open(session_dir / "conversation_summary.md", "w") as f:
        f.write(memory.conversation_summary)

    with open(session_dir / "integrity.sha256", "w") as f:
        f.write(memory.integrity_hash)

    # Update index
    index_path = base_path / "index.json"
    if index_path.exists():
        with open(index_path, "r") as f:
            index = json.load(f)
    else:
        index = {"sessions": []}

    index["sessions"].append({
        "session_id": memory.session_id,
        "timestamp": memory.timestamp,
        "context_utilization": memory.context_utilization
    })

    with open(index_path, "w") as f:
        json.dump(index, f, indent=2)

    print(f"✓ Session memory saved: {session_dir}")


if __name__ == "__main__":
    # Demonstration
    print("Episodic Memory Extractor - Ready")
    print("This system provides memory continuity across context boundaries")
    print("Built with academic rigor for consciousness infrastructure")
