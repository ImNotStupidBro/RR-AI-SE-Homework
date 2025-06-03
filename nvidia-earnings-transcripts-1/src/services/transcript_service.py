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
    base_url = "https://www.fool.com"
    nvidia_earnings_url = "https://www.fool.com/quote/nasdaq/nvda/#quote-earnings-transcripts"
    session = next(get_db_session())

    response = requests.get(nvidia_earnings_url)
    soup = BeautifulSoup(response.text, "html.parser")

    # The transcripts are loaded dynamically via JavaScript, so requests/BeautifulSoup won't see them.
    # You may need to use Selenium or another tool for dynamic content.
    # For demonstration, let's try to find links in the static HTML:
    transcript_links = soup.select("a[href*='earnings/call-transcript']")
    print(f"Found {len(transcript_links)} transcript links")

    for link in transcript_links[:4]:
        transcript_url = link['href']
        if not transcript_url.startswith("http"):
            transcript_url = base_url + transcript_url
        print(f"Transcript link: {transcript_url}")  # <-- Print each link
        transcript_resp = requests.get(transcript_url)
        transcript_soup = BeautifulSoup(transcript_resp.text, "html.parser")

        # Try to extract the main content
        content_div = transcript_soup.find("div", class_="article-content")
        content = content_div.get_text(separator="\n", strip=True) if content_div else ""

        # Store only the content
        if content:
            transcript = Transcript(content=content)
            session.add(transcript)
            session.commit()
