-- =============================================================================
-- The Hero Foundry - Database Initialization Script
-- =============================================================================
-- This script initializes the database with basic structure and sample data
-- Run this after the database container is started

-- Create extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "btree_gin";

-- Set timezone
SET timezone = 'UTC';

-- Create custom types
DO $$ BEGIN
    CREATE TYPE character_mode AS ENUM ('balanced', 'free-for-all');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE character_status AS ENUM ('draft', 'active', 'archived');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

DO $$ BEGIN
    CREATE TYPE ruleset_priority AS ENUM ('core', 'third-party', 'homebrew');
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Create base tables
CREATE TABLE IF NOT EXISTS rulesets (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    version VARCHAR(50) NOT NULL,
    description TEXT,
    priority ruleset_priority NOT NULL DEFAULT 'core',
    content_schema JSONB NOT NULL,
    balance_rules JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS characters (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    level INTEGER NOT NULL DEFAULT 1,
    ruleset_id VARCHAR(50) NOT NULL REFERENCES rulesets(id),
    race_data JSONB NOT NULL,
    class_data JSONB NOT NULL,
    abilities JSONB NOT NULL,
    proficiencies JSONB NOT NULL,
    equipment JSONB NOT NULL,
    spells JSONB,
    features JSONB NOT NULL,
    mode character_mode NOT NULL DEFAULT 'balanced',
    status character_status NOT NULL DEFAULT 'draft',
    version INTEGER NOT NULL DEFAULT 1,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS character_snapshots (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_id UUID NOT NULL REFERENCES characters(id) ON DELETE CASCADE,
    level INTEGER NOT NULL,
    snapshot_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS homebrew_content (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) NOT NULL, -- 'race', 'class', 'spell', 'item', etc.
    content_data JSONB NOT NULL,
    ruleset_id VARCHAR(50) NOT NULL REFERENCES rulesets(id),
    creator_name VARCHAR(255),
    is_balanced BOOLEAN NOT NULL DEFAULT false,
    balance_score DECIMAL(3,2), -- 0.00 to 1.00
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS ai_chat_sessions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    character_id UUID REFERENCES characters(id) ON DELETE SET NULL,
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    context JSONB,
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Create indexes for performance
CREATE INDEX IF NOT EXISTS idx_characters_ruleset ON characters(ruleset_id);
CREATE INDEX IF NOT EXISTS idx_characters_mode ON characters(mode);
CREATE INDEX IF NOT EXISTS idx_characters_status ON characters(status);
CREATE INDEX IF NOT EXISTS idx_characters_created_at ON characters(created_at);

CREATE INDEX IF NOT EXISTS idx_character_snapshots_character ON character_snapshots(character_id);
CREATE INDEX IF NOT EXISTS idx_character_snapshots_level ON character_snapshots(level);

CREATE INDEX IF NOT EXISTS idx_homebrew_content_type ON homebrew_content(type);
CREATE INDEX IF NOT EXISTS idx_homebrew_content_ruleset ON homebrew_content(ruleset_id);
CREATE INDEX IF NOT EXISTS idx_homebrew_content_balanced ON homebrew_content(is_balanced);

CREATE INDEX IF NOT EXISTS idx_ai_chat_sessions_character ON ai_chat_sessions(character_id);
CREATE INDEX IF NOT EXISTS idx_ai_chat_sessions_created_at ON ai_chat_sessions(created_at);

-- Create full-text search indexes
CREATE INDEX IF NOT EXISTS idx_characters_name_search ON characters USING gin(to_tsvector('english', name));
CREATE INDEX IF NOT EXISTS idx_homebrew_content_search ON homebrew_content USING gin(to_tsvector('english', name));

-- Create updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create triggers for updated_at
CREATE TRIGGER update_characters_updated_at BEFORE UPDATE ON characters
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_rulesets_updated_at BEFORE UPDATE ON rulesets
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_homebrew_content_updated_at BEFORE UPDATE ON homebrew_content
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert default D&D 5e ruleset
INSERT INTO rulesets (id, name, version, description, priority, content_schema, balance_rules, metadata) VALUES (
    'dnd5e',
    'Dungeons & Dragons 5th Edition',
    '5.1',
    'Official D&D 5e ruleset based on SRD 5.1 content',
    'core',
    '{
        "races": ["human", "elf", "dwarf", "halfling", "dragonborn", "tiefling", "gnome", "half-elf", "half-orc"],
        "classes": ["fighter", "wizard", "cleric", "rogue", "ranger", "paladin", "barbarian", "bard", "druid", "monk", "sorcerer", "warlock"],
        "backgrounds": ["acolyte", "criminal", "folk-hero", "noble", "sage", "soldier"],
        "equipment": ["weapons", "armor", "adventuring-gear", "tools", "mounts", "vehicles"]
    }',
    '{
        "racial_trait_budget": 7,
        "class_feature_curve": "linear",
        "spell_access_caps": {"cantrips": 4, "1st": 4, "2nd": 3, "3rd": 2},
        "equipment_value_limit": 200
    }',
    '{
        "source": "SRD 5.1",
        "license": "OGL 1.0a",
        "compatibility": ["balanced", "free-for-all"]
    }'
) ON CONFLICT (id) DO NOTHING;

-- Create test user (for development only)
DO $$ BEGIN
    CREATE USER hero_foundry_test WITH PASSWORD 'test_password';
    GRANT ALL PRIVILEGES ON DATABASE hero_foundry TO hero_foundry_test;
    GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hero_foundry_test;
    GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hero_foundry_test;
EXCEPTION
    WHEN duplicate_object THEN null;
END $$;

-- Grant permissions to hero_foundry user
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO hero_foundry;
GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO hero_foundry;
GRANT ALL PRIVILEGES ON ALL FUNCTIONS IN SCHEMA public TO hero_foundry;

-- Create a test character for development
INSERT INTO characters (id, name, level, ruleset_id, race_data, class_data, abilities, proficiencies, equipment, spells, features, mode, metadata) VALUES (
    '550e8400-e29b-41d4-a716-446655440000',
    'Test Character',
    1,
    'dnd5e',
    '{"name": "Human", "traits": ["Extra Feat", "Skill Versatility"]}',
    '{"name": "Fighter", "hit_die": 10, "proficiencies": ["light-armor", "medium-armor", "heavy-armor", "shields", "simple-weapons", "martial-weapons"]}',
    '{"strength": 16, "dexterity": 14, "constitution": 16, "intelligence": 10, "wisdom": 12, "charisma": 8}',
    '{"skills": ["athletics", "perception"], "weapons": ["longsword", "crossbow"], "armor": ["chain-mail"], "languages": ["common", "orc"]}',
    '{"weapons": ["longsword", "crossbow"], "armor": ["chain-mail"], "items": ["backpack", "bedroll", "rations"], "currency": {"gp": 10}}',
    '[]',
    '{"racial": ["Extra Feat", "Skill Versatility"], "class": ["Fighting Style", "Second Wind"], "background": ["Feature"]}',
    'balanced',
    '{"created_by": "development", "notes": "Test character for development environment"}'
) ON CONFLICT (id) DO NOTHING;

-- Create a test homebrew content item
INSERT INTO homebrew_content (id, name, type, content_data, ruleset_id, creator_name, is_balanced, balance_score, metadata) VALUES (
    '660e8400-e29b-41d4-a716-446655440001',
    'Custom Race: Shadow Elf',
    'race',
    '{
        "name": "Shadow Elf",
        "description": "A mysterious elven subrace with shadow magic abilities",
        "traits": ["Darkvision 120ft", "Shadow Step", "Elven Weapon Training"],
        "ability_score_increase": {"dexterity": 2, "charisma": 1},
        "age": {"maturity": 100, "lifespan": 750},
        "size": "medium",
        "speed": 30
    }',
    'dnd5e',
    'Development Team',
    true,
    0.85,
    '{"category": "subrace", "compatibility": ["balanced", "free-for-all"], "notes": "Test homebrew content"}'
) ON CONFLICT (id) DO NOTHING;

-- Print completion message
DO $$
BEGIN
    RAISE NOTICE 'Database initialization completed successfully!';
    RAISE NOTICE 'Default ruleset "dnd5e" created';
    RAISE NOTICE 'Test character "Test Character" created';
    RAISE NOTICE 'Test homebrew content "Shadow Elf" created';
    RAISE NOTICE 'All tables, indexes, and triggers created';
END $$;
