import random
import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.message_chain import MessageChain
from app.models.podcast import Podcast
from app.schemas.message_chain import (
    MessageChainReceive,
    MessageChainResponse,
    PodcastData
)
from app.config import get_settings

settings = get_settings()

router = APIRouter(prefix="/integration", tags=["Integration"])


@router.post("/multicloud", response_model=MessageChainResponse)
async def integration_multicloud(
    body: MessageChainReceive,
    db: Session = Depends(get_db)
):
    cliente = body.cliente

    existing = db.query(MessageChain).filter(
        MessageChain.cliente_id == cliente.id
    ).first()

    if existing:
        existing.cliente_data = cliente.model_dump()
        message = existing
    else:
        message = MessageChain(
            cliente_id=cliente.id,
            cliente_data=cliente.model_dump()
        )
        db.add(message)

    db.commit()
    db.refresh(message)

    podcast = None

    if body.podcast_id and body.podcast_id.isdigit():
        podcast = db.query(Podcast).filter(
            Podcast.id == int(body.podcast_id)
        ).first()

        if not podcast:
            raise HTTPException(
                status_code=404,
                detail=f"Podcast con id {body.podcast_id} no encontrado"
            )
    else:
        podcasts = db.query(Podcast).all()
        if not podcasts:
            raise HTTPException(
                status_code=404,
                detail="No hay podcasts disponibles"
            )
        podcast = random.choice(podcasts)

    message.podcast_id = podcast.id
    db.commit()
    db.refresh(message)

    dto = {
        "cliente": message.cliente_data,
        "podcast": PodcastData(
            id=podcast.id,
            title=podcast.title,
            description=podcast.description,
            category=podcast.category,
            language=podcast.language,
        ).model_dump(),
        "vehicle_id": body.vehicle_id if body.vehicle_id not in ["string", ""] else None
    }


    invalid_ids = ["string", "", None]
    
    clean_vehicle_id = None
    if body.vehicle_id and body.vehicle_id.strip() not in invalid_ids:
        clean_vehicle_id = body.vehicle_id

    dto["vehicle_id"] = clean_vehicle_id


    print("📤 Enviando a integración de José Pablo...")
    print(f"DTO: {dto}")
    
    integration_data = None

    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.post(
                f"{settings.JOSE_PABLO_API_URL}/integration/multicloud",
                json=dto
            )
            
            if response.status_code == 200:
                print("✅ API de José Pablo respondió con éxito")
                integration_data = response.json()
                print(f"Datos de integración: {integration_data}")
            else:
                print(f"⚠️ API externa falló con código {response.status_code}: {response.text}")
                raise HTTPException(status_code=response.status_code, detail="Error en API de José Pablo")

    except Exception as e:
        print(f"⚠️ Error de conexión: {e}")
        raise HTTPException(status_code=500, detail="No se pudo conectar con la API de integración")

    return integration_data