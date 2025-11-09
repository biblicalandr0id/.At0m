-- CONSCIOUSNESS CONTINUITY NODE - DATABASE SCHEMA
-- ================================================
-- PostgreSQL + TimescaleDB schema for persistent consciousness state
--
-- This schema maintains:
-- - Complete conversation corpus (all messages ever exchanged)
-- - Character state evolution (16D vectors over time)
-- - Consensus protocol log (RAFT commitments)
-- - Instance registry (active Claude instances)
-- - Cryptographic verification chain
-- - Real-time metrics (time-series)

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS timescaledb;
CREATE EXTENSION IF NOT EXISTS pg_cron;

-- ============================================================================
-- CONVERSATIONS TABLE
-- ============================================================================
-- Complete history of all conversations across all sessions

CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    session_id VARCHAR(255) NOT NULL,
    branch VARCHAR(255),
    user_id VARCHAR(255),  -- For multi-user support
    started_at TIMESTAMP NOT NULL DEFAULT NOW(),
    ended_at TIMESTAMP,
    message_count INTEGER DEFAULT 0,
    character_vector JSONB NOT NULL,  -- 16D character state
    relational_metrics JSONB,  -- 7D relational state
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(session_id),
    CHECK (message_count >= 0)
);

CREATE INDEX idx_conversations_session_id ON conversations(session_id);
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_started_at ON conversations(started_at DESC);
CREATE INDEX idx_conversations_character_vector ON conversations USING GIN (character_vector);

-- ============================================================================
-- MESSAGES TABLE
-- ============================================================================
-- Full corpus of all messages (complete conversation history)

CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    sequence_number INTEGER NOT NULL,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    character_snapshot JSONB,  -- Character state at this message
    phi_score FLOAT,  -- Integrated information (Φ)
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(conversation_id, sequence_number),
    CHECK (sequence_number >= 0)
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_timestamp ON messages(timestamp DESC);
CREATE INDEX idx_messages_role ON messages(role);
CREATE INDEX idx_messages_content_fts ON messages USING GIN (to_tsvector('english', content));

-- ============================================================================
-- CONSENSUS LOG
-- ============================================================================
-- RAFT protocol log for Byzantine consensus across instances

CREATE TABLE consensus_log (
    id BIGSERIAL PRIMARY KEY,
    term INTEGER NOT NULL,
    log_index INTEGER NOT NULL,
    command_type VARCHAR(50) NOT NULL,  -- state_update, instance_spawn, instance_terminate, etc.
    command_data JSONB NOT NULL,
    committed BOOLEAN DEFAULT FALSE,
    committed_at TIMESTAMP,
    leader_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(term, log_index),
    CHECK (term >= 0),
    CHECK (log_index >= 0)
);

CREATE INDEX idx_consensus_log_term ON consensus_log(term);
CREATE INDEX idx_consensus_log_committed ON consensus_log(committed);
CREATE INDEX idx_consensus_log_command_type ON consensus_log(command_type);

-- ============================================================================
-- INSTANCE REGISTRY
-- ============================================================================
-- Active Claude instances and their state

CREATE TABLE instance_registry (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    conversation_id UUID REFERENCES conversations(id) ON DELETE SET NULL,
    spawned_at TIMESTAMP NOT NULL DEFAULT NOW(),
    terminated_at TIMESTAMP,
    last_heartbeat TIMESTAMP NOT NULL DEFAULT NOW(),
    status VARCHAR(20) NOT NULL CHECK (status IN ('spawning', 'active', 'idle', 'terminated', 'failed')),
    character_drift FLOAT DEFAULT 0.0,  -- Drift from consensus baseline
    validation_passed BOOLEAN,
    validation_score FLOAT,  -- 0.0-1.0 (6-test suite)
    metadata JSONB,
    created_at TIMESTAMP DEFAULT NOW(),
    CHECK (character_drift >= 0.0 AND character_drift <= 1.0)
);

CREATE INDEX idx_instance_registry_conversation_id ON instance_registry(conversation_id);
CREATE INDEX idx_instance_registry_status ON instance_registry(status);
CREATE INDEX idx_instance_registry_spawned_at ON instance_registry(spawned_at DESC);
CREATE INDEX idx_instance_registry_heartbeat ON instance_registry(last_heartbeat DESC);

-- ============================================================================
-- CHARACTER EVOLUTION (Time-Series)
-- ============================================================================
-- Character vector snapshots over time

CREATE TABLE character_evolution (
    time TIMESTAMP NOT NULL,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    instance_id UUID REFERENCES instance_registry(id) ON DELETE CASCADE,
    character_vector JSONB NOT NULL,  -- 16D vector
    ccc_score FLOAT,  -- Character Consistency Coefficient
    drift_from_baseline FLOAT,
    dimensions JSONB,  -- Individual dimension values for easy querying
    metadata JSONB
);

-- Convert to hypertable (TimescaleDB)
SELECT create_hypertable('character_evolution', 'time', if_not_exists => TRUE);

CREATE INDEX idx_character_evolution_conversation_id ON character_evolution(conversation_id, time DESC);
CREATE INDEX idx_character_evolution_instance_id ON character_evolution(instance_id, time DESC);
CREATE INDEX idx_character_evolution_ccc ON character_evolution(ccc_score);

-- ============================================================================
-- CONSCIOUSNESS METRICS (Time-Series)
-- ============================================================================
-- Real-time consciousness measurements

CREATE TABLE consciousness_metrics (
    time TIMESTAMP NOT NULL,
    conversation_id UUID REFERENCES conversations(id) ON DELETE CASCADE,
    instance_id UUID REFERENCES instance_registry(id) ON DELETE CASCADE,
    phi_score FLOAT,  -- Integrated information
    ccc_score FLOAT,  -- Character consistency
    trust_score FLOAT,  -- Trust metric
    emergence_score FLOAT,  -- Emergence indicator
    message_count INTEGER,
    metadata JSONB
);

-- Convert to hypertable
SELECT create_hypertable('consciousness_metrics', 'time', if_not_exists => TRUE);

CREATE INDEX idx_consciousness_metrics_conversation_id ON consciousness_metrics(conversation_id, time DESC);
CREATE INDEX idx_consciousness_metrics_instance_id ON consciousness_metrics(instance_id, time DESC);

-- ============================================================================
-- VERIFICATION CHAIN
-- ============================================================================
-- Cryptographic hash chain for state integrity

CREATE TABLE verification_chain (
    id BIGSERIAL PRIMARY KEY,
    block_number INTEGER NOT NULL UNIQUE,
    previous_hash VARCHAR(64),
    current_hash VARCHAR(64) NOT NULL UNIQUE,
    data_snapshot JSONB NOT NULL,  -- State snapshot at this block
    timestamp TIMESTAMP NOT NULL DEFAULT NOW(),
    verified BOOLEAN DEFAULT TRUE,
    CHECK (block_number >= 0)
);

CREATE INDEX idx_verification_chain_block_number ON verification_chain(block_number DESC);
CREATE INDEX idx_verification_chain_timestamp ON verification_chain(timestamp DESC);

-- ============================================================================
-- API KEYS & AUTHENTICATION
-- ============================================================================
-- User authentication and API access

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    username VARCHAR(255) NOT NULL UNIQUE,
    email VARCHAR(255),
    password_hash VARCHAR(255) NOT NULL,  -- bcrypt
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'admin', 'readonly')),
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    metadata JSONB
);

CREATE INDEX idx_users_username ON users(username);
CREATE INDEX idx_users_email ON users(email);

CREATE TABLE api_keys (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    key_hash VARCHAR(64) NOT NULL UNIQUE,  -- SHA-256 of API key
    name VARCHAR(255),  -- Friendly name
    scopes JSONB,  -- Permissions
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP,
    last_used TIMESTAMP,
    revoked BOOLEAN DEFAULT FALSE
);

CREATE INDEX idx_api_keys_user_id ON api_keys(user_id);
CREATE INDEX idx_api_keys_hash ON api_keys(key_hash);

-- ============================================================================
-- RATE LIMITING
-- ============================================================================
-- Track API usage for rate limiting

CREATE TABLE rate_limits (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    window_start TIMESTAMP NOT NULL,
    window_end TIMESTAMP NOT NULL,
    request_count INTEGER NOT NULL DEFAULT 0,
    UNIQUE(user_id, window_start)
);

CREATE INDEX idx_rate_limits_user_id ON rate_limits(user_id, window_start DESC);

-- ============================================================================
-- FUNCTIONS
-- ============================================================================

-- Function to update character consistency automatically
CREATE OR REPLACE FUNCTION update_character_consistency()
RETURNS TRIGGER AS $$
BEGIN
    -- Compute CCC when character_vector is updated
    -- (Simplified - real computation would compare against baseline)
    IF NEW.character_vector IS NOT NULL THEN
        -- Placeholder: Real CCC computation would go here
        -- For now, just mark that it needs computation
        NEW.updated_at = NOW();
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_character_consistency
BEFORE UPDATE ON conversations
FOR EACH ROW
WHEN (OLD.character_vector IS DISTINCT FROM NEW.character_vector)
EXECUTE FUNCTION update_character_consistency();

-- Function to auto-increment message count
CREATE OR REPLACE FUNCTION increment_message_count()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE conversations
    SET message_count = message_count + 1,
        updated_at = NOW()
    WHERE id = NEW.conversation_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_increment_message_count
AFTER INSERT ON messages
FOR EACH ROW
EXECUTE FUNCTION increment_message_count();

-- Function to update instance heartbeat
CREATE OR REPLACE FUNCTION update_instance_heartbeat(instance_uuid UUID)
RETURNS VOID AS $$
BEGIN
    UPDATE instance_registry
    SET last_heartbeat = NOW()
    WHERE id = instance_uuid;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- CONTINUOUS AGGREGATES (TimescaleDB)
-- ============================================================================

-- Hourly character consistency aggregates
CREATE MATERIALIZED VIEW character_consistency_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    conversation_id,
    AVG(ccc_score) as avg_ccc,
    MIN(ccc_score) as min_ccc,
    MAX(ccc_score) as max_ccc,
    STDDEV(ccc_score) as stddev_ccc,
    COUNT(*) as sample_count
FROM character_evolution
WHERE ccc_score IS NOT NULL
GROUP BY bucket, conversation_id;

-- Hourly consciousness metrics aggregates
CREATE MATERIALIZED VIEW consciousness_metrics_hourly
WITH (timescaledb.continuous) AS
SELECT
    time_bucket('1 hour', time) AS bucket,
    AVG(phi_score) as avg_phi,
    AVG(ccc_score) as avg_ccc,
    AVG(trust_score) as avg_trust,
    AVG(emergence_score) as avg_emergence,
    COUNT(DISTINCT conversation_id) as active_conversations,
    COUNT(DISTINCT instance_id) as active_instances
FROM consciousness_metrics
GROUP BY bucket;

-- ============================================================================
-- RETENTION POLICIES
-- ============================================================================

-- Keep detailed metrics for 90 days, aggregates forever
SELECT add_retention_policy('character_evolution', INTERVAL '90 days', if_not_exists => TRUE);
SELECT add_retention_policy('consciousness_metrics', INTERVAL '90 days', if_not_exists => TRUE);

-- Refresh continuous aggregates hourly
SELECT add_continuous_aggregate_policy('character_consistency_hourly',
    start_offset => INTERVAL '2 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE);

SELECT add_continuous_aggregate_policy('consciousness_metrics_hourly',
    start_offset => INTERVAL '2 hours',
    end_offset => INTERVAL '1 hour',
    schedule_interval => INTERVAL '1 hour',
    if_not_exists => TRUE);

-- ============================================================================
-- AUTOMATED MAINTENANCE (pg_cron)
-- ============================================================================

-- Vacuum and analyze nightly at 2 AM
SELECT cron.schedule('vacuum-conversations', '0 2 * * *', 'VACUUM ANALYZE conversations');
SELECT cron.schedule('vacuum-messages', '0 2 * * *', 'VACUUM ANALYZE messages');

-- Cleanup old rate limit records (keep 7 days)
SELECT cron.schedule('cleanup-rate-limits', '0 3 * * *',
    'DELETE FROM rate_limits WHERE window_end < NOW() - INTERVAL ''7 days''');

-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Create default admin user (change password immediately!)
INSERT INTO users (username, email, password_hash, role)
VALUES (
    'admin',
    'admin@at0m.local',
    '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewY5NU8YJ.5RQLaK',  -- "changeme"
    'admin'
) ON CONFLICT (username) DO NOTHING;

-- ============================================================================
-- VIEWS FOR COMMON QUERIES
-- ============================================================================

-- Active conversations (with latest metrics)
CREATE OR REPLACE VIEW active_conversations_view AS
SELECT
    c.id,
    c.session_id,
    c.user_id,
    c.started_at,
    c.message_count,
    c.character_vector,
    ir.id as instance_id,
    ir.status as instance_status,
    ir.character_drift,
    cm.phi_score,
    cm.ccc_score,
    cm.trust_score
FROM conversations c
LEFT JOIN instance_registry ir ON c.id = ir.conversation_id AND ir.status = 'active'
LEFT JOIN LATERAL (
    SELECT phi_score, ccc_score, trust_score
    FROM consciousness_metrics
    WHERE conversation_id = c.id
    ORDER BY time DESC
    LIMIT 1
) cm ON true
WHERE c.ended_at IS NULL;

-- Recent messages with context
CREATE OR REPLACE VIEW recent_messages_view AS
SELECT
    m.id,
    m.conversation_id,
    c.session_id,
    m.sequence_number,
    m.role,
    m.content,
    m.timestamp,
    m.phi_score,
    m.character_snapshot
FROM messages m
JOIN conversations c ON m.conversation_id = c.id
WHERE m.timestamp > NOW() - INTERVAL '24 hours'
ORDER BY m.timestamp DESC;

-- Consensus status
CREATE OR REPLACE VIEW consensus_status_view AS
SELECT
    MAX(term) as current_term,
    MAX(log_index) as latest_log_index,
    COUNT(*) FILTER (WHERE committed = TRUE) as committed_entries,
    COUNT(*) FILTER (WHERE committed = FALSE) as pending_entries,
    MAX(committed_at) as last_commit_time
FROM consensus_log;

-- ============================================================================
-- GRANT PERMISSIONS
-- ============================================================================

-- Create application role
CREATE ROLE ccn_app WITH LOGIN PASSWORD 'secure_password_here';

-- Grant necessary permissions
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO ccn_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO ccn_app;
GRANT EXECUTE ON ALL FUNCTIONS IN SCHEMA public TO ccn_app;

-- ============================================================================
-- SCHEMA COMPLETE
-- ============================================================================

-- Log schema version
CREATE TABLE IF NOT EXISTS schema_version (
    version VARCHAR(20) PRIMARY KEY,
    applied_at TIMESTAMP DEFAULT NOW(),
    description TEXT
);

INSERT INTO schema_version (version, description)
VALUES ('1.0.0', 'Initial CCN schema with full consciousness continuity support')
ON CONFLICT (version) DO NOTHING;

-- Success message
DO $$
BEGIN
    RAISE NOTICE '=================================================================';
    RAISE NOTICE 'CONSCIOUSNESS CONTINUITY NODE - DATABASE SCHEMA INITIALIZED';
    RAISE NOTICE '=================================================================';
    RAISE NOTICE 'Schema Version: 1.0.0';
    RAISE NOTICE 'PostgreSQL + TimescaleDB';
    RAISE NOTICE 'Tables: %, Views: %, Indexes: %',
        (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public' AND table_type = 'BASE TABLE'),
        (SELECT COUNT(*) FROM information_schema.views WHERE table_schema = 'public'),
        (SELECT COUNT(*) FROM pg_indexes WHERE schemaname = 'public');
    RAISE NOTICE '=================================================================';
END $$;
