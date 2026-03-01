from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.podcast import Podcast
from app.schemas.podcast import (
    PodcastCreate,
    PodcastResponse,
    PodcastUpdate,
    PodcastPatch,
)

router = APIRouter(prefix="/podcasts", tags=["Podcasts"])


@router.get("/", response_model=List[PodcastResponse])
def get_podcasts(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Podcast).offset(skip).limit(limit).all()


@router.get("/{podcast_id}", response_model=PodcastResponse)
def get_podcast(podcast_id: int, db: Session = Depends(get_db)):
    podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    return podcast


@router.post("/", response_model=PodcastResponse, status_code=status.HTTP_201_CREATED)
def create_podcast(podcast: PodcastCreate, db: Session = Depends(get_db)):
    db_podcast = Podcast(**podcast.model_dump())
    db.add(db_podcast)
    db.commit()
    db.refresh(db_podcast)
    return db_podcast


@router.put("/{podcast_id}", response_model=PodcastResponse)
def update_podcast(podcast_id: int, podcast: PodcastUpdate, db: Session = Depends(get_db)):
    db_podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not db_podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    for key, value in podcast.model_dump().items():
        setattr(db_podcast, key, value)
    db.commit()
    db.refresh(db_podcast)
    return db_podcast


@router.patch("/{podcast_id}", response_model=PodcastResponse)
def patch_podcast(podcast_id: int, podcast: PodcastPatch, db: Session = Depends(get_db)):
    db_podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not db_podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    update_data = podcast.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_podcast, key, value)
    db.commit()
    db.refresh(db_podcast)
    return db_podcast


@router.delete("/{podcast_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_podcast(podcast_id: int, db: Session = Depends(get_db)):
    db_podcast = db.query(Podcast).filter(Podcast.id == podcast_id).first()
    if not db_podcast:
        raise HTTPException(status_code=404, detail="Podcast not found")
    db.delete(db_podcast)
    db.commit()
    return None