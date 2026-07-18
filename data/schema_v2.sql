-- schema_v2.sql
-- Database schema for FlexWeb playtest console.

-- Create players table (account login/registration)
CREATE TABLE IF NOT EXISTS players (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create characters table (owned by a player)
CREATE TABLE IF NOT EXISTS characters (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    owner_email VARCHAR(255) REFERENCES players(email) ON DELETE SET NULL,
    class VARCHAR(255),
    race VARCHAR(255),
    hp INT DEFAULT 10,
    might VARCHAR(10) DEFAULT 'd4',
    motion VARCHAR(10) DEFAULT 'd4',
    mind VARCHAR(10) DEFAULT 'd4',
    magic VARCHAR(10) DEFAULT 'd4',
    moxie VARCHAR(10) DEFAULT 'd4',
    skills JSONB DEFAULT '[]'::jsonb,
    inventory JSONB DEFAULT '[]'::jsonb,
    log JSONB DEFAULT '[]'::jsonb,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Index for fast lookup on characters
CREATE INDEX IF NOT EXISTS idx_characters_name ON characters(name);
CREATE INDEX IF NOT EXISTS idx_characters_owner ON characters(owner_email);

-- Create powers table
CREATE TABLE IF NOT EXISTS powers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sub VARCHAR(255),
    table_name VARCHAR(255),
    usage VARCHAR(255),
    action VARCHAR(255),
    effect TEXT,
    source VARCHAR(255),
    dropdown TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create magic_items table
CREATE TABLE IF NOT EXISTS magic_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    sub VARCHAR(255),
    table_name VARCHAR(255),
    usage VARCHAR(255),
    action VARCHAR(255),
    effect TEXT,
    source VARCHAR(255),
    dropdown TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create skillsets table
CREATE TABLE IF NOT EXISTS skillsets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    skills JSONB DEFAULT '[]'::jsonb,
    source VARCHAR(255),
    sub VARCHAR(255),
    table_name VARCHAR(255),
    dropdown TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
