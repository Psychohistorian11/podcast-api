from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Any, Optional
from app.database import get_db
from app.models.podcast import Podcast
from app.schemas.podcast import (
    PodcastCreate,
    PodcastResponse,
    PodcastUpdate,
    PodcastPatch,
)

router = APIRouter(prefix="/api/v2/podcasts", tags=["v2 - Podcasts"])


def _attach_external(podcast: Podcast, external_data: Any) -> dict:
    return {
        "id": podcast.id,
        "title": podcast.title,
        "description": podcast.description,
        "category": podcast.category,
        "language": podcast.language,
        "created_at": podcast.created_at,
        "updated_at": podcast.updated_at,
        "external_data": external_data,
    }


@router.get("/", response_model=List[PodcastResponse])
def get_podcasts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    podcasts = db.query(Podcast).offset(skip).limit(limit).all()
    return [_attach_external(p, None) for p in podcasts]


@router.get("/{podcast_id}", response_model=PodcastResponse)
def get_podcast(podcast_id: int, db: Session = Depends(get_db)):
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return _attach_external(podcast, None)


@router.post("/", response_model=PodcastResponse, status_code=status.HTTP_201_CREATED)
def create_podcast(podcast: PodcastCreate, db: Session = Depends(get_db)):
    db_podcast = Podcast(**podcast.model_dump())
    db.add(db_podcast)
    db.commit()
    db.refresh(db_podcast)
    return _attach_external(db_podcast, None)


@router.put("/{podcast_id}", response_model=PodcastResponse)
def update_podcast(podcast_id: int, podcast: PodcastUpdate, db: Session = Depends(get_db)):
    db_podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not db_podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    for key, value in podcast.model_dump().items():
        setattr(db_podcast, key, value)
    db.commit()
    db.refresh(db_podcast)
    return _attach_external(db_podcast, None)


@router.patch("/{podcast_id}", response_model=PodcastResponse)
def patch_podcast(podcast_id: int, podcast: PodcastPatch, db: Session = Depends(get_db)):
    db_podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not db_podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    for key, value in podcast.model_dump(exclude_unset=True).items():
        setattr(db_podcast, key, value)
    db.commit()
    db.refresh(db_podcast)
    return _attach_external(db_podcast, None)


@router.delete("/{podcast_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_podcast(podcast_id: int, db: Session = Depends(get_db)):
    db_podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not db_podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    db.delete(db_podcast)
    db.commit()
    return None