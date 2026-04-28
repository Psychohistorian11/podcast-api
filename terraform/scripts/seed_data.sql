-- ============================================
-- Script 2: Llenar con datos de prueba
-- ============================================

-- Insertar participantes
INSERT INTO participant (name, email, role, bio) VALUES
    ('Carlos Rodríguez', 'carlos@podcast.com', 'host', 'Host principal del podcast de tecnología'),
    ('María López', 'maria@podcast.com', 'guest', 'Experta en inteligencia artificial'),
    ('Juan García', 'juan@podcast.com', 'producer', 'Productor con 5 años de experiencia');

-- Insertar podcasts
INSERT INTO podcast (title, description, category, language) VALUES
    ('Tech Talks Colombia', 'Conversaciones sobre tecnología y desarrollo', 'Tecnología', 'Español'),
    ('DevOps en la Práctica', 'Todo sobre CI/CD, contenedores y la nube', 'DevOps', 'Español'),
    ('Startup Stories', 'Historias de emprendimiento en Latam', 'Negocios', 'Español');

-- Insertar episodios
INSERT INTO episode (title, description, duration_minutes, podcast_id, participant_id) VALUES
    ('Introducción a Kubernetes', 'Qué es K8s y por qué usarlo', 45, 2, 1),
    ('Docker desde cero', 'Contenedores para principiantes', 60, 2, 2),
    ('FastAPI vs Django', 'Comparando frameworks de Python', 35, 1, 1),
    ('CI/CD con GitHub Actions', 'Automatiza tus despliegues', 50, 2, 3);

-- Insertar mensaje de cadena de prueba
INSERT INTO message_chain (cliente_id, cliente_data, podcast_id) VALUES
    (1, '{"id": 1, "nombre": "Ana García", "ingreso_mensual": 3500000, "puntaje_crediticio": 720, "deuda_actual": 500000}', 1);

-- Verificar datos insertados
SELECT 'participants' as tabla, COUNT(*) as total FROM participant
UNION ALL
SELECT 'podcasts', COUNT(*) FROM podcast
UNION ALL
SELECT 'episodes', COUNT(*) FROM episode
UNION ALL
SELECT 'message_chain', COUNT(*) FROM message_chain;