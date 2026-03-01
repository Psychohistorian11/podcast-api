# 🎙️ Podcast API

API RESTful para gestión de podcasts, construida con **FastAPI**, **PostgreSQL** y **Docker**. Incluye pipelines CI/CD con GitHub Actions y despliegue automático a dos ambientes independientes.

## 🚀 Demo en vivo

| Ambiente | URL |
|----------|-----|
| 🧪 Pruebas | [podcast-api-test.onrender.com](https://podcast-api-test.onrender.com) |
| 🚀 Producción | [podcast-api-prod.onrender.com](https://podcast-api-prod.onrender.com) |

> 📝 Agrega `/docs` a la URL para ver la documentación interactiva (Swagger UI).

## 📋 Descripción

Este proyecto implementa una API RESTful con CRUD completo para 3 entidades relacionadas con el mundo de los podcasts. Forma parte de un taller de DevOps enfocado en CI/CD, ambientes de despliegue y buenas prácticas de desarrollo.

### Entidades

| Entidad | Descripción |
|---------|-------------|
| **Participant** | Personas involucradas en los podcasts (hosts, invitados, productores) |
| **Podcast** | Programas de podcast con su información general |
| **Episode** | Episodios individuales vinculados a un podcast y un participante |

### Operaciones por entidad

Cada entidad soporta las siguientes operaciones:

- `GET /` — Listar todos
- `GET /{id}` — Obtener por ID
- `POST /` — Crear
- `PUT /{id}` — Actualizar (completo)
- `PATCH /{id}` — Actualizar (parcial)
- `DELETE /{id}` — Eliminar

## 🛠️ Tech Stack

| Tecnología | Uso |
|-----------|-----|
| [FastAPI](https://fastapi.tiangolo.com/) | Framework web |
| [SQLAlchemy](https://www.sqlalchemy.org/) | ORM para base de datos |
| [PostgreSQL](https://www.postgresql.org/) | Base de datos |
| [Docker](https://www.docker.com/) | Contenedores |
| [GitHub Actions](https://github.com/features/actions) | CI/CD |
| [Render](https://render.com/) | Hosting y despliegue |
| [Pytest](https://pytest.org/) | Testing |

## 📁 Estructura del proyecto

```
podcast-api/
├── app/
│   ├── config.py              # Configuración (variables de entorno)
│   ├── database.py            # Conexión a PostgreSQL
│   ├── main.py                # Punto de entrada de la app
│   ├── models/                # Modelos SQLAlchemy (tablas)
│   │   ├── participant.py
│   │   ├── podcast.py
│   │   └── episode.py
│   ├── schemas/               # Schemas Pydantic (validación)
│   │   ├── participant.py
│   │   ├── podcast.py
│   │   └── episode.py
│   └── routers/               # Endpoints CRUD
│       ├── participant.py
│       ├── podcast.py
│       └── episode.py
├── tests/                     # Pruebas automatizadas
│   ├── conftest.py
│   ├── test_health.py
│   ├── test_participant.py
│   ├── test_podcast.py
│   └── test_episode.py
├── .github/workflows/         # Pipelines CI/CD
│   ├── pipeline-test.yml
│   └── pipeline-production.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── pytest.ini
```

## 🐳 Ejecución local con Docker

```bash
# Clonar el repositorio
git clone https://github.com/Psychohistorian11/podcast-api.git
cd podcast-api

# Levantar la app + base de datos
docker compose up --build

# La API estará disponible en:
# http://localhost:8000
# http://localhost:8000/docs (Swagger UI)
```

## 🧪 Ejecutar pruebas

```bash
# Instalar dependencias
pip install -r requirements.txt

# Correr las pruebas con cobertura
pytest
```

Las pruebas usan SQLite en memoria, no requieren PostgreSQL ni Docker.

## 🔄 Pipelines CI/CD

El proyecto cuenta con 2 pipelines independientes en GitHub Actions:

### Pipeline de Pruebas (`develop`)

Se ejecuta en cada push o PR a `develop`:

1. 📥 Checkout del código
2. 🐍 Configurar Python 3.11
3. 📦 Instalar dependencias
4. 🧪 Ejecutar pruebas automatizadas
5. 📊 Validar cobertura ≥ 60%
6. 🚀 Deploy a ambiente de pruebas

### Pipeline de Producción (`main`)

Se ejecuta en cada push o PR a `main`:

1. 📥 Checkout del código
2. 🐍 Configurar Python 3.11
3. 📦 Instalar dependencias
4. 🧪 Ejecutar pruebas automatizadas
5. 📊 Validar cobertura ≥ 85%
6. 🐳 Validar build Docker
7. 🚀 Deploy a ambiente de producción

### Reglas de calidad

| Regla | Pruebas | Producción |
|-------|:-------:|:----------:|
| Cobertura mínima | ≥ 60% | ≥ 85% |
| Tests con errores | 0 | 0 |
| Si falla → no despliega | ✅ | ✅ |

## 🌍 Ambientes

| | Pruebas | Producción |
|--|---------|------------|
| **Rama** | `develop` | `main` |
| **URL** | podcast-api-test.onrender.com | podcast-api-prod.onrender.com |
| **Base de datos** | `podcast_test_db` | `podcast_prod_db` |
| **Cobertura mínima** | 60% | 85% |
