from pydantic import BaseModel, ConfigDict
from typing import Optional, Any
from datetime import datetime


class ClienteData(BaseModel):
    id: int
    nombre: str
    ingreso_mensual: float
    puntaje_crediticio: int
    deuda_actual: float


class PodcastData(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    category: str
    language: Optional[str] = "Español"


class MessageChainReceive(BaseModel):
    cliente: ClienteData
    podcast_id: Optional[str] = None
    vehicle_id: Optional[str] = None


class MessageChainResponse(BaseModel):
    cliente: ClienteData
    podcast: Optional[PodcastData] = None
    vehicle: Optional[Any] = None

    model_config = ConfigDict(from_attributes=True)


class MessageChainDB(BaseModel):
    id: int
    cliente_id: int
    cliente_data: dict
    podcast_id: Optional[int] = None
    vehiculo_data: Optional[Any] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)