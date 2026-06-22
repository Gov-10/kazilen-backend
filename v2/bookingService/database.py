from sqlalchemy import create_engine, Column, Integer, String, DateTime, Uuid
from sqlalchemy.orm import declarative_base, sessionmaker
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
import os
from dotenv import load_dotenv
load_dotenv()
DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()
class Bookings(Base):
    __tablename__ = "bookings"
    id=Column(Integer, primary_key=True, index=True)
    booking_id=Column(Uuid)
    customer=Column(String)
    worker=Column(String)
    start_time=Column(DateTime, nullable=True)
    end_time=Column(DateTime, nullable=True)
    action=Column(String)
    status=Column(String, default="assigned")
    rating=Column(Integer, default=0)
    feedback=Column(String, default="No feedback")

Base.metadata.create_all(bind=engine)
SQLAlchemyInstrumentor().instrument(engine=engine)

