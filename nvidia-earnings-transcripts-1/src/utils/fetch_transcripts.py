import requests
from sqlalchemy.orm import sessionmaker
from db.database import Session
from models.transcript import Transcript

def fetch_transcripts(api_url):
    response = requests.get(api_url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to fetch transcripts from the API")

def save_transcripts(transcripts):
    session = Session()
    for transcript in transcripts:
        new_transcript = Transcript(
            date=transcript['date'],
            content=transcript['content']
        )
        session.add(new_transcript)
    session.commit()
    session.close()