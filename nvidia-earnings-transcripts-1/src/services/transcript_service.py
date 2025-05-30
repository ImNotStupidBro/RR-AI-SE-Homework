from sqlalchemy.orm import Session
from models.transcript import Transcript
from db.database import get_db_session

def get_transcripts(db: Session):
    return db.query(Transcript).all()

def get_transcript_by_id(transcript_id: int, db: Session):
    return db.query(Transcript).filter(Transcript.id == transcript_id).first()

def add_transcript(transcript_data: dict, db: Session):
    new_transcript = Transcript(**transcript_data)
    db.add(new_transcript)
    db.commit()
    db.refresh(new_transcript)
    return new_transcript

def delete_transcript(transcript_id: int, db: Session):
    transcript = db.query(Transcript).filter(Transcript.id == transcript_id).first()
    if transcript:
        db.delete(transcript)
        db.commit()
        return True
    return False