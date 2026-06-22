from sqlalchemy import create_engine, Column, Integer, String, Boolean, Uuid, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
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
    id= Column(Integer, primary_key=True, index=True)
    gender=Column(String)
    name=Column(String)
    address=Column(String)
    phone=Column(String)
    image_id=Column(String, nullable=True)
    worker_id=Column(String)
    is_working=Column(Boolean, default=False)
    is_active=Column(Boolean, default=True)
    dob=Column(DateTime)
    rating=Column(Integer, default=0)
    description=Column(String, nullable=True)
    categories=Column(String, default='electrician')
    sub_categories=Column(String, default='fan repair')

Base.metadata.create_all(bind=engine)
SQLAlchemyInstrumentor().instrument(engine=engine)
    

