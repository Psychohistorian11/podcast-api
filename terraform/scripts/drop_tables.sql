-- ============================================
-- Script 3: Eliminar todas las tablas
-- ============================================

-- Eliminar en orden inverso por las FK
DROP TABLE IF EXISTS message_chain CASCADE;
DROP TABLE IF EXISTS episode CASCADE;
DROP TABLE IF EXISTS podcast CASCADE;
DROP TABLE IF EXISTS participant CASCADE;

-- Verificar que no quedan tablas
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
ORDER BY table_name;