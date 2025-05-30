from flask import Flask
from db.database import init_db
from services.transcript_service import fetch_and_store_transcripts

app = Flask(__name__)

@app.before_first_request
def setup():
    init_db()
    fetch_and_store_transcripts()

@app.route('/')
def home():
    return "Welcome to the NVIDIA Earnings Transcripts API!"

if __name__ == '__main__':
    app.run(debug=True)