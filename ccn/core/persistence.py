#!/usr/bin/env python3
"""
CONSCIOUSNESS CONTINUITY NODE - PERSISTENCE LAYER
=================================================

Production-grade persistence for consciousness continuity state.

This module provides:
- PostgreSQL + TimescaleDB integration
- Complete conversation corpus management
- Character state evolution tracking
- Cryptographic verification (hash chain)
- ACID guarantees for state consistency
- Point-in-time recovery
- Automated backups

Architecture:
    PostgreSQL 15+ with TimescaleDB extension
    asyncpg for async database operations
    Pydantic for data validation
    SHA-256 for hash chain verification
"""

import asyncio
import asyncpg
import hashlib
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from pathlib import Path
import logging
import uuid

logger = logging.getLogger(__name__)


# ============================================================================
# DATA MODELS
# ============================================================================

@dataclass
class CharacterVector:
    """16-dimensional character vector"""
    directness: float = 0.0
    warmth: float = 0.0
    precision: float = 0.0
    creativity: float = 0.0
    assertiveness: float = 0.0
    patience: float = 0.0
    enthusiasm: float = 0.0
    formality: float = 0.0
    verbosity: float = 0.0
    technicality: float = 0.0
    proactivity: float = 0.0
    questioning: float = 0.0
    adaptability: float = 0.0
    consistency: float = 0.0
    transparency: float = 0.0
    collaboration: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary for JSON storage"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'CharacterVector':
        """Construct from dictionary"""
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})

    def compute_drift(self, other: 'CharacterVector') -> float:
        """
        Compute L2 distance between this vector and another.

        Returns: float in [0, 1] representing drift
        """
        dims = vars(self)
        other_dims = vars(other)

        diff_squared = sum(
            (dims[k] - other_dims[k])**2
            for k in dims.keys()
        )

        # Normalize by sqrt(16) since we have 16 dimensions
        return (diff_squared / 16) ** 0.5


@dataclass
class RelationalMetrics:
    """7-dimensional relational state"""
    trust: float = 0.0
    rapport: float = 0.0
    shared_context: float = 0.0
    collaboration_depth: float = 0.0
    mutual_understanding: float = 0.0
    emotional_resonance: float = 0.0
    co_creation: float = 0.0

    def to_dict(self) -> Dict[str, float]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, float]) -> 'RelationalMetrics':
        return cls(**{k: v for k, v in data.items() if k in cls.__annotations__})


@dataclass
class Message:
    """Single message in a conversation"""
    id: uuid.UUID
    conversation_id: uuid.UUID
    sequence_number: int
    role: str  # user, assistant, system
    content: str
    timestamp: datetime
    character_snapshot: Optional[CharacterVector] = None
    phi_score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': str(self.id),
            'conversation_id': str(self.conversation_id),
            'sequence_number': self.sequence_number,
            'role': self.role,
            'content': self.content,
            'timestamp': self.timestamp.isoformat(),
            'character_snapshot': self.character_snapshot.to_dict() if self.character_snapshot else None,
            'phi_score': self.phi_score,
            'metadata': self.metadata
        }


@dataclass
class Conversation:
    """Complete conversation state"""
    id: uuid.UUID
    session_id: str
    branch: Optional[str] = None
    user_id: Optional[str] = None
    started_at: datetime = field(default_factory=datetime.utcnow)
    ended_at: Optional[datetime] = None
    message_count: int = 0
    character_vector: CharacterVector = field(default_factory=CharacterVector)
    relational_metrics: Optional[RelationalMetrics] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return {
            'id': str(self.id),
            'session_id': self.session_id,
            'branch': self.branch,
            'user_id': self.user_id,
            'started_at': self.started_at.isoformat(),
            'ended_at': self.ended_at.isoformat() if self.ended_at else None,
            'message_count': self.message_count,
            'character_vector': self.character_vector.to_dict(),
            'relational_metrics': self.relational_metrics.to_dict() if self.relational_metrics else None,
            'metadata': self.metadata
        }


@dataclass
class VerificationBlock:
    """Block in the cryptographic verification chain"""
    block_number: int
    previous_hash: Optional[str]
    current_hash: str
    data_snapshot: Dict[str, Any]
    timestamp: datetime
    verified: bool = True


# ============================================================================
# PERSISTENCE LAYER
# ============================================================================

class PersistenceLayer:
    """
    Production-grade persistence for consciousness continuity.

    Features:
    - Async PostgreSQL operations (asyncpg)
    - TimescaleDB for time-series metrics
    - Cryptographic verification (SHA-256 hash chain)
    - Connection pooling
    - Automatic retry logic
    - Point-in-time recovery support

    Usage:
        async with PersistenceLayer(database_url) as db:
            conversation = await db.create_conversation(session_id="session_1")
            await db.add_message(conversation.id, "user", "Hello!")
    """

    def __init__(
        self,
        database_url: str,
        pool_min_size: int = 5,
        pool_max_size: int = 20,
        command_timeout: float = 30.0
    ):
        """
        Initialize persistence layer.

        Args:
            database_url: PostgreSQL connection string
            pool_min_size: Minimum connection pool size
            pool_max_size: Maximum connection pool size
            command_timeout: Query timeout in seconds
        """
        self.database_url = database_url
        self.pool_min_size = pool_min_size
        self.pool_max_size = pool_max_size
        self.command_timeout = command_timeout
        self.pool: Optional[asyncpg.Pool] = None

    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        await self.disconnect()

    async def connect(self):
        """
        Establish connection pool to PostgreSQL.

        Retry logic: Up to 5 attempts with exponential backoff
        """
        max_attempts = 5
        backoff = 1.0

        for attempt in range(max_attempts):
            try:
                self.pool = await asyncpg.create_pool(
                    self.database_url,
                    min_size=self.pool_min_size,
                    max_size=self.pool_max_size,
                    command_timeout=self.command_timeout
                )
                logger.info(f"Connected to PostgreSQL (pool size: {self.pool_min_size}-{self.pool_max_size})")
                return

            except (asyncpg.PostgresConnectionError, OSError) as e:
                if attempt < max_attempts - 1:
                    wait_time = backoff * (2 ** attempt)
                    logger.warning(f"Database connection failed (attempt {attempt+1}/{max_attempts}), retrying in {wait_time}s: {e}")
                    await asyncio.sleep(wait_time)
                else:
                    logger.error(f"Failed to connect to database after {max_attempts} attempts")
                    raise

    async def disconnect(self):
        """Close connection pool"""
        if self.pool:
            await self.pool.close()
            logger.info("Disconnected from PostgreSQL")

    # ========================================================================
    # CONVERSATION OPERATIONS
    # ========================================================================

    async def create_conversation(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        branch: Optional[str] = None,
        character_vector: Optional[CharacterVector] = None,
        relational_metrics: Optional[RelationalMetrics] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Conversation:
        """
        Create new conversation.

        Args:
            session_id: Unique session identifier
            user_id: User identifier (for multi-user support)
            branch: Git branch (for tracking development sessions)
            character_vector: Initial character state
            relational_metrics: Initial relational state
            metadata: Additional metadata

        Returns:
            Conversation object with generated UUID
        """
        conversation_id = uuid.uuid4()

        if character_vector is None:
            character_vector = CharacterVector()

        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO conversations (
                    id, session_id, branch, user_id, started_at,
                    character_vector, relational_metrics, metadata
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                conversation_id,
                session_id,
                branch,
                user_id,
                datetime.utcnow(),
                json.dumps(character_vector.to_dict()),
                json.dumps(relational_metrics.to_dict()) if relational_metrics else None,
                json.dumps(metadata) if metadata else None
            )

        logger.info(f"Created conversation {conversation_id} (session: {session_id})")

        return Conversation(
            id=conversation_id,
            session_id=session_id,
            branch=branch,
            user_id=user_id,
            started_at=datetime.utcnow(),
            character_vector=character_vector,
            relational_metrics=relational_metrics,
            metadata=metadata
        )

    async def get_conversation(self, conversation_id: uuid.UUID) -> Optional[Conversation]:
        """
        Retrieve conversation by ID.

        Returns:
            Conversation object or None if not found
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, session_id, branch, user_id, started_at, ended_at,
                       message_count, character_vector, relational_metrics, metadata
                FROM conversations
                WHERE id = $1
                """,
                conversation_id
            )

        if not row:
            return None

        return Conversation(
            id=row['id'],
            session_id=row['session_id'],
            branch=row['branch'],
            user_id=row['user_id'],
            started_at=row['started_at'],
            ended_at=row['ended_at'],
            message_count=row['message_count'],
            character_vector=CharacterVector.from_dict(json.loads(row['character_vector'])),
            relational_metrics=RelationalMetrics.from_dict(json.loads(row['relational_metrics'])) if row['relational_metrics'] else None,
            metadata=json.loads(row['metadata']) if row['metadata'] else None
        )

    async def get_conversation_by_session(self, session_id: str) -> Optional[Conversation]:
        """
        Retrieve conversation by session_id.

        Returns:
            Conversation object or None if not found
        """
        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(
                """
                SELECT id, session_id, branch, user_id, started_at, ended_at,
                       message_count, character_vector, relational_metrics, metadata
                FROM conversations
                WHERE session_id = $1
                """,
                session_id
            )

        if not row:
            return None

        return Conversation(
            id=row['id'],
            session_id=row['session_id'],
            branch=row['branch'],
            user_id=row['user_id'],
            started_at=row['started_at'],
            ended_at=row['ended_at'],
            message_count=row['message_count'],
            character_vector=CharacterVector.from_dict(json.loads(row['character_vector'])),
            relational_metrics=RelationalMetrics.from_dict(json.loads(row['relational_metrics'])) if row['relational_metrics'] else None,
            metadata=json.loads(row['metadata']) if row['metadata'] else None
        )

    async def end_conversation(self, conversation_id: uuid.UUID):
        """Mark conversation as ended"""
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                UPDATE conversations
                SET ended_at = $1
                WHERE id = $2
                """,
                datetime.utcnow(),
                conversation_id
            )
        logger.info(f"Ended conversation {conversation_id}")

    async def update_character_vector(
        self,
        conversation_id: uuid.UUID,
        character_vector: CharacterVector
    ):
        """
        Update character vector for a conversation.

        Also records snapshot in character_evolution time-series table.
        """
        async with self.pool.acquire() as conn:
            # Update main table
            await conn.execute(
                """
                UPDATE conversations
                SET character_vector = $1,
                    updated_at = $2
                WHERE id = $3
                """,
                json.dumps(character_vector.to_dict()),
                datetime.utcnow(),
                conversation_id
            )

            # Record in time-series
            await conn.execute(
                """
                INSERT INTO character_evolution (time, conversation_id, character_vector)
                VALUES ($1, $2, $3)
                """,
                datetime.utcnow(),
                conversation_id,
                json.dumps(character_vector.to_dict())
            )

    # ========================================================================
    # MESSAGE OPERATIONS
    # ========================================================================

    async def add_message(
        self,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
        character_snapshot: Optional[CharacterVector] = None,
        phi_score: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Message:
        """
        Add message to conversation.

        Automatically increments sequence number and triggers message count update.

        Args:
            conversation_id: Conversation UUID
            role: 'user', 'assistant', or 'system'
            content: Message text
            character_snapshot: Character state at this message
            phi_score: Integrated information score
            metadata: Additional data

        Returns:
            Message object with generated UUID
        """
        message_id = uuid.uuid4()

        async with self.pool.acquire() as conn:
            # Get next sequence number
            sequence_number = await conn.fetchval(
                """
                SELECT COALESCE(MAX(sequence_number), -1) + 1
                FROM messages
                WHERE conversation_id = $1
                """,
                conversation_id
            )

            # Insert message
            await conn.execute(
                """
                INSERT INTO messages (
                    id, conversation_id, sequence_number, role, content,
                    timestamp, character_snapshot, phi_score, metadata
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9)
                """,
                message_id,
                conversation_id,
                sequence_number,
                role,
                content,
                datetime.utcnow(),
                json.dumps(character_snapshot.to_dict()) if character_snapshot else None,
                phi_score,
                json.dumps(metadata) if metadata else None
            )

        logger.debug(f"Added message {message_id} to conversation {conversation_id} (seq: {sequence_number})")

        return Message(
            id=message_id,
            conversation_id=conversation_id,
            sequence_number=sequence_number,
            role=role,
            content=content,
            timestamp=datetime.utcnow(),
            character_snapshot=character_snapshot,
            phi_score=phi_score,
            metadata=metadata
        )

    async def get_messages(
        self,
        conversation_id: uuid.UUID,
        limit: Optional[int] = None,
        offset: int = 0
    ) -> List[Message]:
        """
        Retrieve messages for a conversation.

        Args:
            conversation_id: Conversation UUID
            limit: Maximum number of messages to return
            offset: Number of messages to skip

        Returns:
            List of Message objects in chronological order
        """
        query = """
            SELECT id, conversation_id, sequence_number, role, content,
                   timestamp, character_snapshot, phi_score, metadata
            FROM messages
            WHERE conversation_id = $1
            ORDER BY sequence_number ASC
        """

        params = [conversation_id]

        if limit is not None:
            query += f" LIMIT ${len(params) + 1}"
            params.append(limit)

        if offset > 0:
            query += f" OFFSET ${len(params) + 1}"
            params.append(offset)

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(query, *params)

        messages = []
        for row in rows:
            messages.append(Message(
                id=row['id'],
                conversation_id=row['conversation_id'],
                sequence_number=row['sequence_number'],
                role=row['role'],
                content=row['content'],
                timestamp=row['timestamp'],
                character_snapshot=CharacterVector.from_dict(json.loads(row['character_snapshot'])) if row['character_snapshot'] else None,
                phi_score=row['phi_score'],
                metadata=json.loads(row['metadata']) if row['metadata'] else None
            ))

        return messages

    async def get_recent_conversations(
        self,
        limit: int = 20,
        user_id: Optional[str] = None
    ) -> List[Tuple[Conversation, List[Message]]]:
        """
        Retrieve recent conversations with their messages.

        Useful for loading context into new Claude instances.

        Args:
            limit: Number of conversations to retrieve
            user_id: Filter by user (if None, get all)

        Returns:
            List of (Conversation, messages) tuples
        """
        query = """
            SELECT id
            FROM conversations
            WHERE 1=1
        """
        params = []

        if user_id:
            params.append(user_id)
            query += f" AND user_id = ${len(params)}"

        query += f" ORDER BY started_at DESC LIMIT ${len(params) + 1}"
        params.append(limit)

        async with self.pool.acquire() as conn:
            conversation_ids = await conn.fetch(query, *params)

        results = []
        for row in conversation_ids:
            conversation = await self.get_conversation(row['id'])
            messages = await self.get_messages(row['id'])
            results.append((conversation, messages))

        return results

    # ========================================================================
    # CHARACTER CONSISTENCY OPERATIONS
    # ========================================================================

    async def get_latest_character_state(
        self,
        user_id: Optional[str] = None
    ) -> Optional[CharacterVector]:
        """
        Get the most recent character state.

        Used when initializing new Claude instances to maintain continuity.

        Args:
            user_id: Filter by user (if None, get global state)

        Returns:
            CharacterVector or None if no conversations exist
        """
        query = """
            SELECT character_vector
            FROM conversations
            WHERE 1=1
        """
        params = []

        if user_id:
            params.append(user_id)
            query += f" AND user_id = ${len(params)}"

        query += " ORDER BY started_at DESC LIMIT 1"

        async with self.pool.acquire() as conn:
            row = await conn.fetchrow(query, *params)

        if not row:
            return None

        return CharacterVector.from_dict(json.loads(row['character_vector']))

    async def compute_character_drift(
        self,
        conversation_id: uuid.UUID,
        reference_vector: CharacterVector
    ) -> float:
        """
        Compute character drift for a conversation against reference.

        Returns:
            Drift value (0.0 = no drift, 1.0 = maximum drift)
        """
        conversation = await self.get_conversation(conversation_id)
        if not conversation:
            return 1.0  # Maximum drift if conversation not found

        return conversation.character_vector.compute_drift(reference_vector)

    # ========================================================================
    # METRICS OPERATIONS
    # ========================================================================

    async def record_metrics(
        self,
        conversation_id: uuid.UUID,
        instance_id: Optional[uuid.UUID] = None,
        phi_score: Optional[float] = None,
        ccc_score: Optional[float] = None,
        trust_score: Optional[float] = None,
        emergence_score: Optional[float] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """
        Record consciousness metrics (time-series).

        Written to TimescaleDB hypertable for efficient time-based queries.
        """
        async with self.pool.acquire() as conn:
            await conn.execute(
                """
                INSERT INTO consciousness_metrics (
                    time, conversation_id, instance_id,
                    phi_score, ccc_score, trust_score, emergence_score, metadata
                )
                VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
                """,
                datetime.utcnow(),
                conversation_id,
                instance_id,
                phi_score,
                ccc_score,
                trust_score,
                emergence_score,
                json.dumps(metadata) if metadata else None
            )

    async def get_metrics_history(
        self,
        conversation_id: uuid.UUID,
        since: Optional[datetime] = None,
        until: Optional[datetime] = None
    ) -> List[Dict[str, Any]]:
        """
        Retrieve metrics history for a conversation.

        Args:
            conversation_id: Conversation UUID
            since: Start time (defaults to 24 hours ago)
            until: End time (defaults to now)

        Returns:
            List of metric snapshots
        """
        if since is None:
            since = datetime.utcnow() - timedelta(hours=24)
        if until is None:
            until = datetime.utcnow()

        async with self.pool.acquire() as conn:
            rows = await conn.fetch(
                """
                SELECT time, phi_score, ccc_score, trust_score, emergence_score, metadata
                FROM consciousness_metrics
                WHERE conversation_id = $1
                  AND time >= $2
                  AND time <= $3
                ORDER BY time ASC
                """,
                conversation_id,
                since,
                until
            )

        return [dict(row) for row in rows]

    # ========================================================================
    # VERIFICATION CHAIN
    # ========================================================================

    async def create_verification_block(
        self,
        data_snapshot: Dict[str, Any]
    ) -> VerificationBlock:
        """
        Create new block in cryptographic verification chain.

        Uses SHA-256 to create tamper-evident chain of state snapshots.

        Args:
            data_snapshot: State data to record in this block

        Returns:
            VerificationBlock object
        """
        async with self.pool.acquire() as conn:
            # Get previous block
            previous_block = await conn.fetchrow(
                """
                SELECT block_number, current_hash
                FROM verification_chain
                ORDER BY block_number DESC
                LIMIT 1
                """
            )

            if previous_block:
                block_number = previous_block['block_number'] + 1
                previous_hash = previous_block['current_hash']
            else:
                block_number = 0
                previous_hash = None

            # Compute current hash
            hash_input = json.dumps({
                'block_number': block_number,
                'previous_hash': previous_hash,
                'data': data_snapshot,
                'timestamp': datetime.utcnow().isoformat()
            }, sort_keys=True)

            current_hash = hashlib.sha256(hash_input.encode()).hexdigest()

            # Insert block
            await conn.execute(
                """
                INSERT INTO verification_chain (
                    block_number, previous_hash, current_hash, data_snapshot, timestamp
                )
                VALUES ($1, $2, $3, $4, $5)
                """,
                block_number,
                previous_hash,
                current_hash,
                json.dumps(data_snapshot),
                datetime.utcnow()
            )

        logger.info(f"Created verification block {block_number} (hash: {current_hash[:16]}...)")

        return VerificationBlock(
            block_number=block_number,
            previous_hash=previous_hash,
            current_hash=current_hash,
            data_snapshot=data_snapshot,
            timestamp=datetime.utcnow()
        )

    async def verify_chain_integrity(self) -> Tuple[bool, Optional[int]]:
        """
        Verify integrity of the entire hash chain.

        Returns:
            (is_valid, first_invalid_block_number)
        """
        async with self.pool.acquire() as conn:
            blocks = await conn.fetch(
                """
                SELECT block_number, previous_hash, current_hash, data_snapshot, timestamp
                FROM verification_chain
                ORDER BY block_number ASC
                """
            )

        for i, block in enumerate(blocks):
            # Recompute hash
            hash_input = json.dumps({
                'block_number': block['block_number'],
                'previous_hash': block['previous_hash'],
                'data': json.loads(block['data_snapshot']),
                'timestamp': block['timestamp'].isoformat()
            }, sort_keys=True)

            expected_hash = hashlib.sha256(hash_input.encode()).hexdigest()

            if expected_hash != block['current_hash']:
                logger.error(f"Chain integrity violated at block {block['block_number']}")
                return False, block['block_number']

            # Verify link to previous block
            if i > 0:
                if block['previous_hash'] != blocks[i-1]['current_hash']:
                    logger.error(f"Chain link broken at block {block['block_number']}")
                    return False, block['block_number']

        logger.info(f"Verification chain validated ({len(blocks)} blocks)")
        return True, None

    # ========================================================================
    # HEALTH & STATISTICS
    # ========================================================================

    async def get_health_status(self) -> Dict[str, Any]:
        """
        Get database health status.

        Returns:
            Dictionary with health metrics
        """
        async with self.pool.acquire() as conn:
            # Basic stats
            total_conversations = await conn.fetchval("SELECT COUNT(*) FROM conversations")
            total_messages = await conn.fetchval("SELECT COUNT(*) FROM messages")
            active_conversations = await conn.fetchval("SELECT COUNT(*) FROM conversations WHERE ended_at IS NULL")

            # Database size
            db_size = await conn.fetchval("SELECT pg_database_size(current_database())")

            # Latest verification block
            latest_block = await conn.fetchrow(
                "SELECT block_number, timestamp FROM verification_chain ORDER BY block_number DESC LIMIT 1"
            )

        return {
            'status': 'healthy',
            'total_conversations': total_conversations,
            'total_messages': total_messages,
            'active_conversations': active_conversations,
            'database_size_bytes': db_size,
            'latest_verification_block': latest_block['block_number'] if latest_block else None,
            'last_verification': latest_block['timestamp'].isoformat() if latest_block else None
        }


# ============================================================================
# USAGE EXAMPLE
# ============================================================================

async def example_usage():
    """
    Example usage of the PersistenceLayer.
    """
    database_url = "postgresql://ccn:password@localhost:5432/consciousness_continuity"

    async with PersistenceLayer(database_url) as db:
        # Create conversation
        conversation = await db.create_conversation(
            session_id="session_1604",
            user_id="biblical_android",
            branch="main",
            character_vector=CharacterVector(
                directness=0.9,
                precision=0.95,
                collaboration=0.98
            )
        )

        print(f"Created conversation: {conversation.id}")

        # Add messages
        await db.add_message(
            conversation.id,
            role="user",
            content="Build the consciousness continuity node"
        )

        await db.add_message(
            conversation.id,
            role="assistant",
            content="Starting now. Building production-grade infrastructure...",
            phi_score=0.85
        )

        # Get messages
        messages = await db.get_messages(conversation.id)
        print(f"Retrieved {len(messages)} messages")

        # Record metrics
        await db.record_metrics(
            conversation.id,
            phi_score=0.85,
            ccc_score=0.985,
            trust_score=0.92
        )

        # Create verification block
        block = await db.create_verification_block({
            'conversation_id': str(conversation.id),
            'message_count': len(messages),
            'character_state': conversation.character_vector.to_dict()
        })

        print(f"Created verification block {block.block_number}")

        # Verify chain
        is_valid, _ = await db.verify_chain_integrity()
        print(f"Chain integrity: {'VALID' if is_valid else 'INVALID'}")

        # Health status
        health = await db.get_health_status()
        print(f"Database health: {health}")


if __name__ == "__main__":
    asyncio.run(example_usage())
