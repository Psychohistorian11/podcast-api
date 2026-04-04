import logging
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.podcast import Podcast

logger = logging.getLogger("podcast-api")

router = APIRouter(prefix="/api/v2", tags=["v2 - Chain"])


def _get_podcast(db: Session) -> dict:
    """
    Obtiene el primer podcast disponible en la base de datos.
    Como la DB se consulta en cada llamada, cualquier cambio
    hecho via PATCH/PUT se refleja inmediatamente en el chain.
    """
    podcast = db.query(Podcast).first()
    if not podcast:
        return {
            "id": None,
            "title": "No podcast available",
            "description": None,
            "category": None,
            "language": None,
            "source_api": "podcast-api",
            "cloud": "AWS App Runner",
        }
    return {
        "id": podcast.id,
        "title": podcast.title,
        "description": podcast.description,
        "category": podcast.category,
        "language": podcast.language,
        "source_api": "podcast-api",
        "cloud": "AWS App Runner",
    }


@router.post("/chain")
async def chain_message(
    payload: dict = {},
    db: Session = Depends(get_db),
):
    """
    Último eslabón de la cadena multicloud.

    Recibe el payload acumulado de Simón (GCP) y Jose Pablo (GCP/K8s),
    agrega el Podcast de esta API y retorna la respuesta final completa.

    Respuesta esperada:
    {
        "[entidad_simon]":      { ... },   <- llegó de Simón
        "[entidad_jose_pablo]": { ... },   <- llegó de Jose Pablo
        "podcast":              { ... }    <- agregado aquí
    }
    """
    logger.info(f"Chain received — keys in payload: {list(payload.keys())}")

    podcast_data = _get_podcast(db)

    final_response = {
        **payload,
        "podcast": podcast_data,
    }

    logger.info(f"Chain complete — returning final response with keys: {list(final_response.keys())}")
    return final_response


@router.get("/chain/info")
def chain_info():
    """
    Diagnóstico: muestra la posición y configuración
    de esta API dentro de la cadena multicloud.
    """
    return {
        "api": "podcast-api",
        "version": "2.0.0",
        "entity": "Podcast",
        "cloud": "AWS App Runner",
        "position": "3 de 3 — último en la cadena",
        "receives_from": "Jose Pablo (GCP / Kubernetes)",
        "next_api": "ninguna — retorna respuesta final",
        "endpoints_v2": {
            "chain":         "POST   /api/v2/chain",
            "chain_info":    "GET    /api/v2/chain/info",
            "list":          "GET    /api/v2/podcasts",
            "get_by_id":     "GET    /api/v2/podcasts/{id}",
            "create":        "POST   /api/v2/podcasts",
            "update":        "PUT    /api/v2/podcasts/{id}",
            "partial_update":"PATCH  /api/v2/podcasts/{id}",
            "delete":        "DELETE /api/v2/podcasts/{id}",
        },
    }