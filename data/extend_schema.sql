-- extend_schema.sql
-- Add attributes to characters table
ALTER TABLE characters ADD COLUMN IF NOT EXISTS might VARCHAR(10) DEFAULT 'd4';
ALTER TABLE characters ADD COLUMN IF NOT EXISTS motion VARCHAR(10) DEFAULT 'd4';
ALTER TABLE characters ADD COLUMN IF NOT EXISTS mind VARCHAR(10) DEFAULT 'd4';
ALTER TABLE characters ADD COLUMN IF NOT EXISTS magic VARCHAR(10) DEFAULT 'd4';
ALTER TABLE characters ADD COLUMN IF NOT EXISTS moxie VARCHAR(10) DEFAULT 'd4';
ALTER TABLE characters ADD COLUMN IF NOT EXISTS skills JSONB DEFAULT '[]'::jsonb;

-- Create powers table
CREATE TABLE IF NOT EXISTS powers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    usage VARCHAR(255),
    action VARCHAR(255),
    effect TEXT,
    source VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create magic_items table
CREATE TABLE IF NOT EXISTS magic_items (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    usage VARCHAR(255),
    action VARCHAR(255),
    effect TEXT,
    source VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Create skillsets table
CREATE TABLE IF NOT EXISTS skillsets (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    skills JSONB DEFAULT '[]'::jsonb,
    source VARCHAR(255),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
