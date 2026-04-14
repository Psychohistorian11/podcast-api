import httpx
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.message_chain import MessageChain
from app.models.podcast import Podcast
from app.schemas.message_chain import MessageChainResponse, MessageChainReceive, PodcastData
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/v2/chain", tags=["v2 - Chain"])


@router.post("/receive", status_code=status.HTTP_201_CREATED)
def receive_from_ScoreBank(body: MessageChainReceive, db: Session = Depends(get_db)):
    """
    Recibe entidad Cliente y la guarda en message_chain
    con podcast y vehiculo en null.
    """

    cliente = body.cliente

    existing = db.query(MessageChain).filter(
        MessageChain.cliente_id == cliente.id
    ).first()

    if existing:
        existing.cliente_data = cliente.model_dump()
        existing.podcast_id = None
        existing.vehiculo_data = None
        db.commit()
        db.refresh(existing)
        message = existing
    else:
        message = MessageChain(
            cliente_id=cliente.id,
            cliente_data=cliente.model_dump(),
            podcast_id=None,
            vehiculo_data=None
        )
        db.add(message)
        db.commit()
        db.refresh(message)

    return {
        "status": "received",
        "message_id": message.id,
        "cliente": message.cliente_data,
        "podcast": None,
        "vehiculo": None
    }


@router.post("/send/{podcast_id}", response_model=MessageChainResponse)
async def send_to_VehicleAPI(podcast_id: int, db: Session = Depends(get_db)):
    """
    Endpoint que el usuario llama pasando el podcast_id.
    1. Busca el último mensaje recibido
    2. Hace GET a ScoreBanckAPI para traer datos frescos del cliente
    3. Actualiza en DB si hay cambios
    4. Adjunta el Podcast
    5. Envía todo a terceraAPI
    """

    # 1. Buscar el mensaje más reciente
    message = db.query(MessageChain).order_by(
        MessageChain.created_at.desc()
    ).first()

    if not message:
        raise HTTPException(
            status_code=404,
            detail="No hay mensajes recibidos de Simón aún. Llama primero a /receive"
        )

    # 2. GET a la API de ScoreBanck para traer datos frescos
    cliente_id = message.cliente_id
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(
                f"{settings.SIMON_API_URL}/api/v2/clientes/{cliente_id}"
            )
            if response.status_code == 200:
                fresh_cliente = response.json()

                # 3. Verificar si algo cambió y actualizar si es necesario
                if fresh_cliente != message.cliente_data:
                    message.cliente_data = fresh_cliente
                    db.commit()
                    db.refresh(message)

    except Exception as e:
        # Si ScoreBanck no responde, continuamos con los datos que tenemos
        # No bloqueamos la cadena por esto
        print(f"⚠️ No se pudo conectar a ScoreBanck: {e}. Usando datos guardados.")

    # 4. Buscar el Podcast
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not podcast:
        raise HTTPException(
            status_code=404,
            detail=f"Podcast con id {podcast_id} no encontrado"
        )

    # 5. Actualizar el mensaje con el podcast
    message.podcast_id = podcast.id
    db.commit()
    db.refresh(message)

    # 6. Construir el DTO completo
    dto = {
        "cliente": message.cliente_data,
        "podcast": PodcastData(
            id=podcast.id,
            title=podcast.title,
            description=podcast.description,
            category=podcast.category,
            language=podcast.language,
        ),
        "vehiculo": None
    }

    # 7. Enviar a VehicleAPI si tiene URL configurada
    if settings.JOSE_PABLO_API_URL:
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                jose_response = await client.post(
                    f"{settings.JOSE_PABLO_API_URL}/api/v2/chain/receive",
                    json=dto
                )
                print(f"✅ Enviado a VehicleAPI: {jose_response.status_code}")
        except Exception as e:
            print(f"⚠️ No se pudo enviar a VehicleAPI: {e}")

    return dto