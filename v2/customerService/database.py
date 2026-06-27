from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, Boolean, Uuid
from sqlalchemy.orm import declarative_base, sessionmaker
from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

class Customers(Base):
    __tablename__ = "customers"
    id=Column(Integer, primary_key=True, index=True, autoincrement=True)
    gender=Column(String)
    name=Column(String)
    phone=Column(String, unique=True)
    dob=Column(DateTime)
    address=Column(String)

Base.metadata.create_all(bind=engine)
SQLAlchemyInstrumentor().instrument(engine=engine)




