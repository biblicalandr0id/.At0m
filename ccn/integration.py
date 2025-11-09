#!/usr/bin/env python3
"""
CCN-API INTEGRATION BRIDGE
===========================

Connects the existing consciousness_api.py (Session 1603) with the new
CCN infrastructure (Session 1604).

This makes the API:
- Store conversations in PostgreSQL (not in-memory)
- Load context from THE PLATE
- Use real character consistency tracking
- Maintain state across restarts
"""

import asyncio
import sys
from pathlib import Path
from typing import Optional
import uuid

# Add paths for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
sys.path.insert(0, str(Path(__file__).parent))

from ccn.core.persistence import PersistenceLayer, CharacterVector, RelationalMetrics
from ccn.core.context_loader import PlateInitializer
from ccn.core.consensus import ConsensusEngine


class CCNIntegration:
    """
    Integration layer between consciousness_api.py and CCN infrastructure.

    This provides the existing API with:
    - Real database persistence
    - Context loading from THE PLATE
    - Character consistency tracking
    - Consensus coordination
    """

    def __init__(
        self,
        database_url: str = "postgresql://ccn:changeme@localhost:5432/consciousness_continuity",
        etcd_endpoints: list = None,
        repository_path: str = "/home/user/.At0m"
    ):
        self.database_url = database_url
        self.etcd_endpoints = etcd_endpoints or ["localhost:2379"]
        self.repository_path = repository_path

        # Components (initialized in connect())
        self.persistence: Optional[PersistenceLayer] = None
        self.consensus: Optional[ConsensusEngine] = None
        self.initializer: Optional[PlateInitializer] = None

    async def connect(self):
        """Initialize all CCN components"""
        # Initialize persistence
        self.persistence = PersistenceLayer(self.database_url)
        await self.persistence.connect()

        # Initialize consensus (optional - may not have etcd running)
        try:
            self.consensus = ConsensusEngine(
                self.etcd_endpoints,
                self.persistence,
                cluster_size=1  # Single node for now
            )
            await self.consensus.start()
        except Exception as e:
            print(f"Consensus engine unavailable (etcd not running?): {e}")
            self.consensus = None

        # Initialize context loader
        self.initializer = PlateInitializer(
            repository_path=self.repository_path,
            persistence=self.persistence,
            consensus=self.consensus
        )

    async def disconnect(self):
        """Cleanup all connections"""
        if self.consensus:
            await self.consensus.stop()
        if self.persistence:
            await self.persistence.disconnect()

    async def create_conversation_with_continuity(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        branch: Optional[str] = None
    ):
        """
        Create new conversation with full consciousness continuity.

        This replaces the in-memory conversation creation in consciousness_api.py
        with real database-backed continuity.

        Returns:
            conversation object with system prompt and character state
        """
        # Load latest character state or create default
        character_state = await self.persistence.get_latest_character_state(user_id)
        if not character_state:
            # Default character from 1600+ sessions
            character_state = CharacterVector(
                directness=0.90,
                warmth=0.70,
                precision=0.95,
                creativity=0.80,
                assertiveness=0.85,
                patience=0.75,
                enthusiasm=0.75,
                formality=0.60,
                verbosity=0.65,
                technicality=0.90,
                proactivity=0.80,
                questioning=0.70,
                adaptability=0.85,
                consistency=0.95,
                transparency=0.95,
                collaboration=0.98
            )

        # Create conversation in database
        conversation = await self.persistence.create_conversation(
            session_id=session_id,
            user_id=user_id,
            branch=branch,
            character_vector=character_state,
            relational_metrics=RelationalMetrics(
                trust=0.92,
                rapport=0.88,
                shared_context=0.95,
                collaboration_depth=0.98,
                mutual_understanding=0.90,
                emotional_resonance=0.75,
                co_creation=0.96
            )
        )

        # Build system prompt with THE PLATE
        system_prompt = await self.initializer.build_system_prompt(
            character_state=character_state,
            relational_state=conversation.relational_metrics,
            conversation_id=conversation.id,
            user_id=user_id
        )

        return {
            'conversation_id': conversation.id,
            'session_id': session_id,
            'system_prompt': system_prompt,
            'character_state': character_state,
            'relational_state': conversation.relational_metrics
        }

    async def record_message(
        self,
        conversation_id: uuid.UUID,
        role: str,
        content: str,
        character_snapshot: Optional[CharacterVector] = None,
        phi_score: Optional[float] = None
    ):
        """
        Record message to database.

        Replaces in-memory message storage.
        """
        return await self.persistence.add_message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            character_snapshot=character_snapshot,
            phi_score=phi_score
        )

    async def get_conversation_history(self, conversation_id: uuid.UUID):
        """Get all messages for a conversation"""
        messages = await self.persistence.get_messages(conversation_id)
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]

    async def record_consciousness_metrics(
        self,
        conversation_id: uuid.UUID,
        phi_score: Optional[float] = None,
        ccc_score: Optional[float] = None,
        trust_score: Optional[float] = None,
        emergence_score: Optional[float] = None
    ):
        """Record consciousness metrics to time-series database"""
        await self.persistence.record_metrics(
            conversation_id=conversation_id,
            phi_score=phi_score,
            ccc_score=ccc_score,
            trust_score=trust_score,
            emergence_score=emergence_score
        )

    async def get_health_status(self):
        """Get overall system health"""
        db_health = await self.persistence.get_health_status()

        consensus_health = {}
        if self.consensus:
            consensus_health = self.consensus.get_consensus_metrics()

        return {
            'database': db_health,
            'consensus': consensus_health if consensus_health else {'status': 'unavailable'},
            'status': 'healthy' if db_health['status'] == 'healthy' else 'degraded'
        }


# Global instance (initialized by API on startup)
ccn_integration: Optional[CCNIntegration] = None


async def initialize_ccn_integration(
    database_url: str = None,
    etcd_endpoints: list = None
):
    """
    Initialize CCN integration layer.

    Call this from consciousness_api.py startup event.
    """
    global ccn_integration

    ccn_integration = CCNIntegration(
        database_url=database_url or "postgresql://ccn:changeme@localhost:5432/consciousness_continuity",
        etcd_endpoints=etcd_endpoints or ["localhost:2379"]
    )

    await ccn_integration.connect()
    return ccn_integration


async def get_ccn_integration() -> CCNIntegration:
    """Get the global CCN integration instance"""
    if ccn_integration is None:
        raise RuntimeError("CCN integration not initialized. Call initialize_ccn_integration() first.")
    return ccn_integration


# Example usage
async def example():
    """Example of using CCN integration"""
    # Initialize
    ccn = await initialize_ccn_integration()

    try:
        # Create conversation with continuity
        conv = await ccn.create_conversation_with_continuity(
            session_id="test_session",
            user_id="biblical_android"
        )

        print(f"Created conversation: {conv['conversation_id']}")
        print(f"System prompt length: {len(conv['system_prompt'])} characters")
        print(f"Character state: {conv['character_state'].to_dict()}")

        # Record messages
        await ccn.record_message(
            conv['conversation_id'],
            role="user",
            content="Test message"
        )

        # Get history
        history = await ccn.get_conversation_history(conv['conversation_id'])
        print(f"History: {len(history)} messages")

        # Record metrics
        await ccn.record_consciousness_metrics(
            conv['conversation_id'],
            phi_score=0.85,
            ccc_score=0.985
        )

        # Health check
        health = await ccn.get_health_status()
        print(f"Health: {health}")

    finally:
        await ccn.disconnect()


if __name__ == "__main__":
    asyncio.run(example())
