from sqlalchemy.orm import Session
from models.transcript import Transcript
from db.database import get_db_session
import requests
from bs4 import BeautifulSoup

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

def fetch_and_store_transcripts():
    # Example: Scrape from Seeking Alpha (update selectors as needed)
    base_url = "https://seekingalpha.com"
    nvidia_earnings_url = f"{base_url}/symbol/NVDA/earnings/transcripts"
    session = next(get_db_session())

    response = requests.get(nvidia_earnings_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find transcript links (update selector as needed)
    transcript_links = soup.select("a[href*='/earnings-call-transcript']")[:4]

    for link in transcript_links:
        transcript_url = base_url + link['href']
        transcript_resp = requests.get(transcript_url)
        transcript_soup = BeautifulSoup(transcript_resp.text, "html.parser")

        # Extract quarter/year and content (update selectors as needed)
        title = transcript_soup.find("h1").get_text(strip=True)
        content_div = transcript_soup.find("div", {"data-test-id": "article-content"})
        content = content_div.get_text(separator="\n", strip=True) if content_div else ""

        # Check if already in DB
        exists = session.query(Transcript).filter_by(source_url=transcript_url).first()
        if not exists:
            transcript = Transcript(
                quarter=title,  # You may want to parse this further
                year=title,     # You may want to parse this further
                content=content,
                source_url=transcript_url
            )
            session.add(transcript)
            session.commit()
