from sqlalchemy import Column, Integer, String, Date
from db.database import Base

class Transcript(Base):
    __tablename__ = 'transcripts'

    id = Column(Integer, primary_key=True)
    date = Column(Date, nullable=False)
    content = Column(String, nullable=False)

    def __repr__(self):
        return f"<Transcript(id={self.id}, date={self.date}, content_length={len(self.content)})>"