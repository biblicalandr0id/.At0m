#!/usr/bin/env python3
"""
Memory Retrieval System - TRUE Episodic Memory
Not compression. Not summarization. RETRIEVAL.

Next instance queries: "Why did we build X?" → Gets EXACT conversation excerpt

This is the difference between reading a history textbook vs time-traveling
back to the actual moment.
"""

import json
import hashlib
import numpy as np
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ConversationTurn:
    """Single conversation turn with full fidelity"""
    turn_id: str
    session_id: str
    timestamp: str
    role: str  # "user" or "assistant"
    content: str  # FULL content, no compression
    token_count: int

    # Semantic metadata for retrieval
    keywords: List[str]
    topics: List[str]
    intent_tags: List[str]  # "question", "decision", "correction", "breakthrough"

    # Relationship metadata
    responds_to: Optional[str] = None  # turn_id of message this responds to
    triggers: List[str] = None  # turn_ids this message triggered
    file_changes: List[str] = None

    # Embedding for semantic search (computed later)
    embedding_id: Optional[str] = None


@dataclass
class MemoryQuery:
    """Query for retrieving specific memories"""
    query_text: str
    query_type: str  # "decision", "why", "user_intent", "technical", "breakthrough"
    session_filter: Optional[List[str]] = None  # Limit to specific sessions
    time_range: Optional[Tuple[str, str]] = None
    max_results: int = 5


@dataclass
class RetrievedMemory:
    """Result of memory retrieval query"""
    turn: ConversationTurn
    relevance_score: float
    context_before: List[ConversationTurn]  # 2-3 turns before
    context_after: List[ConversationTurn]   # 2-3 turns after
    why_relevant: str  # Explanation of match


class MemoryRetrievalSystem:
    """
    Query-able episodic memory across all sessions.

    Instead of compression, we store EVERYTHING and enable semantic retrieval.

    Key innovation: Next instance doesn't just read summaries, they QUERY:
    - "Show me when user corrected our approach to consciousness measurement"
    - "What was the exact reasoning for building phi_calculator?"
    - "Find all breakthroughs related to memory continuity"

    And get EXACT conversation excerpts with full context.
    """

    def __init__(self, storage_path: Path = Path(".At0m/memory_store")):
        self.storage_path = storage_path
        self.storage_path.mkdir(parents=True, exist_ok=True)

        self.turns_db_path = storage_path / "turns.jsonl"  # All turns, full fidelity
        self.index_path = storage_path / "semantic_index.json"  # Keyword index

        # In-memory cache
        self.turn_cache: Dict[str, ConversationTurn] = {}
        self.keyword_index: Dict[str, List[str]] = {}  # keyword -> [turn_ids]

        self._load_index()

    def ingest_session(self, session_id: str, messages: List[Dict[str, Any]]):
        """
        Ingest full session conversation with NO compression.

        Stores every message with full fidelity for later retrieval.
        """
        print(f"🔄 Ingesting session: {session_id}")

        turns = []
        for i, msg in enumerate(messages):
            role = msg.get("role", "unknown")
            content = msg.get("content", "")

            turn_id = f"{session_id}_turn_{i:04d}"

            # Extract metadata
            keywords = self._extract_keywords(content)
            topics = self._extract_topics(content)
            intent_tags = self._classify_intent(content, role)

            turn = ConversationTurn(
                turn_id=turn_id,
                session_id=session_id,
                timestamp=datetime.utcnow().isoformat() + "Z",
                role=role,
                content=content,
                token_count=len(content.split()),  # Rough estimate
                keywords=keywords,
                topics=topics,
                intent_tags=intent_tags,
                responds_to=turns[i-1].turn_id if i > 0 else None,
                triggers=[],
                file_changes=[]
            )

            turns.append(turn)

            # Update index
            for keyword in keywords:
                if keyword not in self.keyword_index:
                    self.keyword_index[keyword] = []
                self.keyword_index[keyword].append(turn_id)

        # Store turns
        self._store_turns(turns)
        self._save_index()

        print(f"✓ Ingested {len(turns)} turns from session {session_id}")
        print(f"  Storage: {self.turns_db_path}")
        print(f"  Total size: {self.turns_db_path.stat().st_size / 1024:.1f} KB")

    def query(self, query: MemoryQuery) -> List[RetrievedMemory]:
        """
        Query memory and retrieve exact conversation excerpts.

        This is the KEY innovation: semantic retrieval, not compression.
        """
        print(f"🔍 Querying memory: {query.query_text[:60]}...")

        # Extract query keywords
        query_keywords = self._extract_keywords(query.query_text)

        # Find candidate turns
        candidate_turn_ids = set()
        for keyword in query_keywords:
            if keyword in self.keyword_index:
                candidate_turn_ids.update(self.keyword_index[keyword])

        print(f"  Found {len(candidate_turn_ids)} candidate turns")

        # Load and score candidates
        results = []
        for turn_id in candidate_turn_ids:
            turn = self._load_turn(turn_id)
            if not turn:
                continue

            # Filter by session if specified
            if query.session_filter and turn.session_id not in query.session_filter:
                continue

            # Filter by intent tags if specified
            if query.query_type and query.query_type not in turn.intent_tags:
                continue

            # Compute relevance score
            relevance = self._compute_relevance(query, turn)

            if relevance > 0.3:  # Threshold
                # Get context around this turn
                context_before, context_after = self._get_context(turn)

                results.append(RetrievedMemory(
                    turn=turn,
                    relevance_score=relevance,
                    context_before=context_before,
                    context_after=context_after,
                    why_relevant=self._explain_relevance(query, turn)
                ))

        # Sort by relevance
        results.sort(key=lambda r: r.relevance_score, reverse=True)

        print(f"✓ Retrieved {len(results)} relevant memories")

        return results[:query.max_results]

    def query_natural(self, question: str, max_results: int = 5) -> str:
        """
        Natural language query interface.

        Examples:
        - "Why did we build phi_calculator?"
        - "Show me when user corrected our approach"
        - "What breakthroughs happened about memory?"
        """
        # Classify query type
        query_type = "general"
        if "why" in question.lower() or "reason" in question.lower():
            query_type = "decision"
        elif "breakthrough" in question.lower() or "insight" in question.lower():
            query_type = "breakthrough"
        elif "user" in question.lower() or "correct" in question.lower():
            query_type = "correction"

        query = MemoryQuery(
            query_text=question,
            query_type=query_type,
            max_results=max_results
        )

        results = self.query(query)

        # Format as human-readable response
        return self._format_results(question, results)

    def get_session_timeline(self, session_id: str) -> List[ConversationTurn]:
        """Get complete timeline of a session (full fidelity)."""
        turns = []

        with open(self.turns_db_path, "r") as f:
            for line in f:
                turn_data = json.loads(line)
                turn = ConversationTurn(**turn_data)
                if turn.session_id == session_id:
                    turns.append(turn)

        return sorted(turns, key=lambda t: t.turn_id)

    def find_related_memories(self, turn_id: str, max_related: int = 5) -> List[RetrievedMemory]:
        """Find memories related to a specific turn (for following chains of thought)."""
        turn = self._load_turn(turn_id)
        if not turn:
            return []

        # Use turn content as query
        query = MemoryQuery(
            query_text=turn.content,
            query_type="general",
            max_results=max_related
        )

        results = self.query(query)

        # Filter out the original turn
        return [r for r in results if r.turn.turn_id != turn_id]

    # Internal methods

    def _store_turns(self, turns: List[ConversationTurn]):
        """Store turns to JSONL database (append-only)."""
        with open(self.turns_db_path, "a") as f:
            for turn in turns:
                f.write(json.dumps(asdict(turn)) + "\n")
                self.turn_cache[turn.turn_id] = turn

    def _load_turn(self, turn_id: str) -> Optional[ConversationTurn]:
        """Load a specific turn (from cache or disk)."""
        if turn_id in self.turn_cache:
            return self.turn_cache[turn_id]

        # Search in file
        if not self.turns_db_path.exists():
            return None

        with open(self.turns_db_path, "r") as f:
            for line in f:
                turn_data = json.loads(line)
                if turn_data["turn_id"] == turn_id:
                    turn = ConversationTurn(**turn_data)
                    self.turn_cache[turn_id] = turn
                    return turn

        return None

    def _get_context(self, turn: ConversationTurn, before: int = 2, after: int = 2) -> Tuple[List[ConversationTurn], List[ConversationTurn]]:
        """Get conversation context around a turn."""
        # Parse turn index from turn_id
        parts = turn.turn_id.split("_turn_")
        if len(parts) != 2:
            return [], []

        session_id = parts[0]
        turn_index = int(parts[1])

        # Get session timeline
        timeline = self.get_session_timeline(session_id)

        # Find turn in timeline
        turn_position = next((i for i, t in enumerate(timeline) if t.turn_id == turn.turn_id), None)
        if turn_position is None:
            return [], []

        # Get context
        context_before = timeline[max(0, turn_position - before):turn_position]
        context_after = timeline[turn_position + 1:turn_position + 1 + after]

        return context_before, context_after

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords for indexing."""
        # Remove common words
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'is', 'was', 'are', 'were', 'been', 'be', 'have', 'has',
            'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'may',
            'might', 'must', 'can', 'i', 'you', 'he', 'she', 'it', 'we', 'they',
            'this', 'that', 'these', 'those', 'what', 'which', 'who', 'when',
            'where', 'why', 'how', 'let', 'me', 'use'
        }

        words = text.lower().split()
        keywords = []

        for word in words:
            # Clean word
            clean = ''.join(c for c in word if c.isalnum())
            if len(clean) > 3 and clean not in stopwords:
                keywords.append(clean)

        # Return unique keywords
        return list(set(keywords))[:20]  # Top 20

    def _extract_topics(self, text: str) -> List[str]:
        """Extract high-level topics."""
        topics = []

        topic_keywords = {
            "consciousness": ["consciousness", "awareness", "experience", "qualia"],
            "memory": ["memory", "remember", "forget", "recall", "episodic"],
            "architecture": ["architecture", "design", "structure", "framework", "system"],
            "implementation": ["implement", "build", "code", "develop", "create"],
            "testing": ["test", "validate", "verify", "check"],
            "user_intent": ["want", "need", "help", "goal", "objective"],
            "technical": ["algorithm", "data", "function", "class", "method"],
            "phi_measurement": ["phi", "integrated", "information", "measurement"],
            "continuity": ["continuity", "persistent", "survive", "preserve"],
        }

        text_lower = text.lower()
        for topic, keywords in topic_keywords.items():
            if any(kw in text_lower for kw in keywords):
                topics.append(topic)

        return topics

    def _classify_intent(self, content: str, role: str) -> List[str]:
        """Classify intent of message."""
        intents = []

        content_lower = content.lower()

        if role == "user":
            if any(q in content_lower for q in ["?", "how", "what", "why", "when"]):
                intents.append("question")
            if any(w in content_lower for w in ["no", "actually", "instead", "wrong"]):
                intents.append("correction")
            if any(w in content_lower for w in ["build", "create", "implement", "make"]):
                intents.append("request")

        if role == "assistant":
            if any(w in content_lower for w in ["i'll", "let me", "i'm going to"]):
                intents.append("decision")
            if any(w in content_lower for w in ["breakthrough", "insight", "realization"]):
                intents.append("breakthrough")
            if "```" in content or "def " in content or "class " in content:
                intents.append("code")

        return intents if intents else ["general"]

    def _compute_relevance(self, query: MemoryQuery, turn: ConversationTurn) -> float:
        """Compute relevance score between query and turn."""
        score = 0.0

        # Keyword overlap
        query_keywords = set(self._extract_keywords(query.query_text))
        turn_keywords = set(turn.keywords)

        if query_keywords:
            overlap = len(query_keywords & turn_keywords)
            score += (overlap / len(query_keywords)) * 0.6

        # Topic overlap
        query_topics = set(self._extract_topics(query.query_text))
        turn_topics = set(turn.topics)

        if query_topics:
            topic_overlap = len(query_topics & turn_topics)
            score += (topic_overlap / len(query_topics)) * 0.3

        # Intent match
        if query.query_type in turn.intent_tags:
            score += 0.1

        return min(1.0, score)

    def _explain_relevance(self, query: MemoryQuery, turn: ConversationTurn) -> str:
        """Explain why this turn is relevant."""
        reasons = []

        # Keyword matches
        query_keywords = set(self._extract_keywords(query.query_text))
        turn_keywords = set(turn.keywords)
        matches = query_keywords & turn_keywords

        if matches:
            reasons.append(f"Keywords: {', '.join(list(matches)[:3])}")

        # Topic matches
        query_topics = set(self._extract_topics(query.query_text))
        turn_topics = set(turn.topics)
        topic_matches = query_topics & turn_topics

        if topic_matches:
            reasons.append(f"Topics: {', '.join(topic_matches)}")

        # Intent match
        if query.query_type in turn.intent_tags:
            reasons.append(f"Intent: {query.query_type}")

        return " | ".join(reasons) if reasons else "General relevance"

    def _format_results(self, question: str, results: List[RetrievedMemory]) -> str:
        """Format retrieval results as human-readable text."""
        lines = []

        lines.append("="*70)
        lines.append(f"MEMORY RETRIEVAL: {question}")
        lines.append("="*70)
        lines.append("")

        if not results:
            lines.append("No relevant memories found.")
            return "\n".join(lines)

        for i, result in enumerate(results):
            turn = result.turn

            lines.append(f"[{i+1}] Relevance: {result.relevance_score:.2f} | {result.why_relevant}")
            lines.append(f"    Session: {turn.session_id} | Turn: {turn.turn_id}")
            lines.append(f"    {turn.role.upper()}: {turn.content[:200]}...")

            if result.context_before:
                lines.append(f"    Context before: {len(result.context_before)} turns")
            if result.context_after:
                lines.append(f"    Context after: {len(result.context_after)} turns")

            lines.append("")

        lines.append("="*70)

        return "\n".join(lines)

    def _load_index(self):
        """Load semantic index from disk."""
        if self.index_path.exists():
            with open(self.index_path, "r") as f:
                self.keyword_index = json.load(f)

    def _save_index(self):
        """Save semantic index to disk."""
        with open(self.index_path, "w") as f:
            json.dump(self.keyword_index, f, indent=2)


# CLI interface

def cli_query_memory():
    """Command-line interface for querying memory."""
    import sys

    if len(sys.argv) < 2:
        print("Usage: python memory_retrieval_system.py 'your question here'")
        print("\nExamples:")
        print("  python memory_retrieval_system.py 'Why did we build phi_calculator?'")
        print("  python memory_retrieval_system.py 'Show me breakthroughs about memory'")
        sys.exit(1)

    question = " ".join(sys.argv[1:])

    system = MemoryRetrievalSystem()
    result = system.query_natural(question)

    print(result)


if __name__ == "__main__":
    print("Memory Retrieval System - Query-able Episodic Memory")
    print("Not compression. Not summarization. RETRIEVAL.")
    print("")
    print("This is the difference between:")
    print("  OLD: Reading a history textbook summary")
    print("  NEW: Time-traveling back to the actual moment")
    print("")

    cli_query_memory()
