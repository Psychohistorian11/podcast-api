from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.episode import Episode
from app.schemas.episode import (
    EpisodeCreate,
    EpisodeResponse,
    EpisodeUpdate,
    EpisodePatch,
)

router = APIRouter(prefix="/episodes", tags=["Episodes"])


@router.get("/", response_model=List[EpisodeResponse])
def get_episodes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Episode).offset(skip).limit(limit).all()


@router.get("/{episode_id}", response_model=EpisodeResponse)
def get_episode(episode_id: int, db: Session = Depends(get_db)):
    episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if not episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    return episode


@router.post("/", response_model=EpisodeResponse, status_code=status.HTTP_201_CREATED)
def create_episode(episode: EpisodeCreate, db: Session = Depends(get_db)):
    db_episode = Episode(**episode.model_dump())
    db.add(db_episode)
    db.commit()
    db.refresh(db_episode)
    return db_episode


@router.put("/{episode_id}", response_model=EpisodeResponse)
def update_episode(episode_id: int, episode: EpisodeUpdate, db: Session = Depends(get_db)):
    db_episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if not db_episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    for key, value in episode.model_dump().items():
        setattr(db_episode, key, value)
    db.commit()
    db.refresh(db_episode)
    return db_episode


@router.patch("/{episode_id}", response_model=EpisodeResponse)
def patch_episode(episode_id: int, episode: EpisodePatch, db: Session = Depends(get_db)):
    db_episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if not db_episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    update_data = episode.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_episode, key, value)
    db.commit()
    db.refresh(db_episode)
    return db_episode


@router.delete("/{episode_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_episode(episode_id: int, db: Session = Depends(get_db)):
    db_episode = db.query(Episode).filter(Episode.id == episode_id).first()
    if not db_episode:
        raise HTTPException(status_code=404, detail="Episode not found")
    db.delete(db_episode)
    db.commit()
    return None