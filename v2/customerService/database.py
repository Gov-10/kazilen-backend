from sqlalchemy import create_engine, Column, Integer, String, DateTime, func, Boolean, Uuid
from sqlalchemy.orm import declarative_base, sessionmaker
import os
from dotenv import load_dotenv
load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
engine=create_engine(DATABASE_URL)
sessionLocal=sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base=declarative_base()

class Customers(Base):
    __tablename__ = "customers"
    id=Column(Integer, primary_key=True, index=True)
    gender=Column(String)
    name=Column(String)
    phone=Column(String, unique=True, primary_key=True)
    dob=Column(DateTime)
    address=Column(String)




