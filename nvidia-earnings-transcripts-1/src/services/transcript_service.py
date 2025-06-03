from sqlalchemy.orm import Session
from models.transcript import Transcript
from db.database import get_db_session
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
import time
from datetime import datetime

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

    # Set up headless Edge
    edge_options = EdgeOptions()
    edge_options.add_argument("--headless")
    driver = None

    try:
        try:
            driver = webdriver.Edge(options=edge_options)
        except Exception as e:
            print("Could not start Edge WebDriver. Make sure msedgedriver.exe is installed and in your PATH.")
            print("Error details:", e)
            return

        driver.get(nvidia_earnings_url)
        time.sleep(5)  # Wait for JS to load content

        links = driver.find_elements(By.XPATH, "//a[contains(@href, 'earnings-call-transcript')]")
        print(f"Found {len(links)} transcript links")

        # Extract URLs first to avoid stale element reference
        transcript_urls = [link.get_attribute('href') for link in links[:4]]

        for transcript_url in transcript_urls:
            print(f"Transcript link: {transcript_url}")
            driver.get(transcript_url)
            # time.sleep(2)
            try:
                # print(driver.page_source)
                content_div = driver.find_element(By.CLASS_NAME, "article-body")
                content = content_div.text
            except Exception as e:
                print(f"Could not extract content from {transcript_url}: {e}")
                content = ""

            # After extracting 'content', also extract 'date' from the page
            try:
                date_element = driver.find_element(By.ID, "date")  # Replace with the actual class or selector
                date_text = date_element.text  # Parse/format as needed
            except Exception as e:
                print(f"Could not extract date from {transcript_url}: {e}")
                date_text = ""

            if content and date_text:
                print(f"Extracted content length: {len(content)}")
                # Parse the date string to a date object
                date_obj = datetime.strptime(date_text, "%b %d, %Y").date()
                transcript = Transcript(content=content, date=date_obj)
                session.add(transcript)
                session.commit()
    finally:
        if driver:
            driver.quit()
