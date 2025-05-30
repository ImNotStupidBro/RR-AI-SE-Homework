from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///nvidia_transcripts.db"  # Change this to your preferred database URL

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def init_db():
    from models import transcript  # Ensure model is imported
    Base.metadata.create_all(bind=engine)
def get_db_session():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()