from flask import Flask, render_template
from db.database import init_db, get_db_session
from services.transcript_service import fetch_and_store_transcripts
from models.transcript import Transcript

app = Flask(__name__)

@app.route('/')
def home():
    session = next(get_db_session())
    transcripts = session.query(Transcript).order_by(Transcript.id.desc()).limit(4).all()
    return render_template('index.html', transcripts=transcripts)

if __name__ == '__main__':
    init_db()
    fetch_and_store_transcripts()
    app.run(debug=True)