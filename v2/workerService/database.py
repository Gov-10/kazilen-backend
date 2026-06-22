from sqlalchemy import create_engine, Column, Integer, String, Boolean, Uuid, Date, JSON, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.sql import func
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()
class Workers(Base):
    __tablename__ = "workers"
    id= Column(Integer, primary_key=True, index=True, autoincrement=True)
    gender=Column(String)
    name=Column(String)
    address=Column(String)
    phone=Column(String, unique=True)
    image_id=Column(String, nullable=True)
    worker_id=Column(String, unique=True)
    is_working=Column(Boolean, default=False)
    is_active=Column(Boolean, default=True)
    dob=Column(Date)
    created_all=Column(DateTime(timezone=True), server_default=func.now())
    rating=Column(Integer, default=0)
    description=Column(String, nullable=True)
    categories=Column(String, default='NA')
    sub_categories=Column(JSON, default=list)

Base.metadata.create_all(bind=engine)
SQLAlchemyInstrumentor().instrument(engine=engine)
    

