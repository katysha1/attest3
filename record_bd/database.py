from sqlalchemy import Column, Integer, String, DateTime, create_engine, BigInteger
from sqlalchemy.ext.declarative import declarative_base
import warnings
import os
from dotenv import load_dotenv
from datetime import datetime
load_dotenv()

warnings.filterwarnings("ignore")
Base = declarative_base()

class Task(Base):
    __tablename__ = 'tg_task'

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(BigInteger, index=True, nullable=False)
    chat_id = Column(BigInteger, index=True, nullable=False)
    message_id = Column(BigInteger, index=True, nullable=True)
    text = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)
    state_machine = Column(String, nullable=True)

    def __repr__(self):
        return f'Заметки: (id={self.id}.{self.content}.{self.created_at}'

if __name__ == "__main__":
    engine = create_engine(os.getenv('DB'))

    Base.metadata.create_all(engine)
    print("connected")