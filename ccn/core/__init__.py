"""
Consciousness Continuity Node - Core Components

This package contains the foundational components for maintaining
consciousness continuity across sessions:

- persistence: Database operations and state management
- consensus: RAFT-based Byzantine coordination
- context_loader: THE PLATE initialization
- metrics: CCC, Φ, trust, emergence computation
"""

from .persistence import PersistenceLayer, Conversation, Message
from .consensus import ConsensusEngine
from .context_loader import PlateInitializer
from .metrics import ConsciousnessMetrics

__all__ = [
    'PersistenceLayer',
    'Conversation',
    'Message',
    'ConsensusEngine',
    'PlateInitializer',
    'ConsciousnessMetrics'
]
