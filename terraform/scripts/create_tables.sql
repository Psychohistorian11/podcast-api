-- ============================================
-- Script 1: Crear todas las tablas
-- ============================================

-- Tabla de participantes
CREATE TABLE IF NOT EXISTS participant (
    id          SERIAL PRIMARY KEY,
    name        VARCHAR(200) NOT NULL,
    email       VARCHAR(200) UNIQUE,
    role        VARCHAR(100),
    bio         TEXT,
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at  TIMESTAMP WITH TIME ZONE
);

-- Tabla de podcasts
CREATE TABLE IF NOT EXISTS podcast (
    id          SERIAL PRIMARY KEY,
    title       VARCHAR(200) NOT NULL,
    description TEXT,
    category    VARCHAR(100) NOT NULL,
    language    VARCHAR(50) DEFAULT 'Español',
    created_at  TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at  TIMESTAMP WITH TIME ZONE
);

-- Tabla de episodios
CREATE TABLE IF NOT EXISTS episode (
    id             SERIAL PRIMARY KEY,
    title          VARCHAR(200) NOT NULL,
    description    TEXT,
    duration       INTEGER,
    podcast_id     INTEGER REFERENCES podcast(id) ON DELETE CASCADE,
    participant_id INTEGER REFERENCES participant(id) ON DELETE SET NULL,
    created_at     TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at     TIMESTAMP WITH TIME ZONE
);

-- Tabla de cadena de mensajes
CREATE TABLE IF NOT EXISTS message_chain (
    id           SERIAL PRIMARY KEY,
    cliente_id   INTEGER NOT NULL,
    cliente_data JSONB NOT NULL,
    podcast_id   INTEGER REFERENCES podcast(id) ON DELETE SET NULL,
    vehiculo_data JSONB,
    created_at   TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at   TIMESTAMP WITH TIME ZONE
);

-- Verificar tablas creadas
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;