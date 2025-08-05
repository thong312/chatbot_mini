from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
import os

# Kết nối DB (ví dụ user=postgres, pass=123)
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:12345@localhost:5432/chatbot")

engine = create_engine(DATABASE_URL)
Base = declarative_base()

class ChatHistory(Base):
    __tablename__ = "chat_history"
    id = Column(Integer, primary_key=True)
    role = Column(String(50))  # 'user' hoặc 'bot'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)
SessionLocal = sessionmaker(bind=engine)

def save_message(role, content):
    session = SessionLocal()
    msg = ChatHistory(role=role, content=content)
    session.add(msg)
    session.commit()
    session.close()

def get_history(limit=20):
    session = SessionLocal()
    history = session.query(ChatHistory).order_by(ChatHistory.timestamp.desc()).limit(limit).all()
    session.close()
    return history
