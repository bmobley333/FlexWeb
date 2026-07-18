-- schema.sql
-- Database schema for FlexWeb playtest console.

-- Create characters table
CREATE TABLE IF NOT EXISTS characters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    class VARCHAR(255),
    race VARCHAR(255),
    hp INT DEFAULT 10,
    inventory JSONB DEFAULT '[]'::jsonb,
    log JSONB DEFAULT '[]'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index on name for fast lookups
CREATE INDEX IF NOT EXISTS idx_characters_name ON characters(name);
