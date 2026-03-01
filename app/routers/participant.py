from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.participant import Participant
from app.schemas.participant import (
    ParticipantCreate,
    ParticipantResponse,
    ParticipantUpdate,
    ParticipantPatch,
)

router = APIRouter(prefix="/participants", tags=["Participants"])


@router.get("/", response_model=List[ParticipantResponse])
def get_participants(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(Participant).offset(skip).limit(limit).all()


@router.get("/{participant_id}", response_model=ParticipantResponse)
def get_participant(participant_id: int, db: Session = Depends(get_db)):
    participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if not participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    return participant


@router.post("/", response_model=ParticipantResponse, status_code=status.HTTP_201_CREATED)
def create_participant(participant: ParticipantCreate, db: Session = Depends(get_db)):
    db_participant = Participant(**participant.model_dump())
    db.add(db_participant)
    db.commit()
    db.refresh(db_participant)
    return db_participant


@router.put("/{participant_id}", response_model=ParticipantResponse)
def update_participant(participant_id: int, participant: ParticipantUpdate, db: Session = Depends(get_db)):
    db_participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    for key, value in participant.model_dump().items():
        setattr(db_participant, key, value)
    db.commit()
    db.refresh(db_participant)
    return db_participant


@router.patch("/{participant_id}", response_model=ParticipantResponse)
def patch_participant(participant_id: int, participant: ParticipantPatch, db: Session = Depends(get_db)):
    db_participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    update_data = participant.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_participant, key, value)
    db.commit()
    db.refresh(db_participant)
    return db_participant


@router.delete("/{participant_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_participant(participant_id: int, db: Session = Depends(get_db)):
    db_participant = db.query(Participant).filter(Participant.id == participant_id).first()
    if not db_participant:
        raise HTTPException(status_code=404, detail="Participant not found")
    db.delete(db_participant)
    db.commit()
    return None