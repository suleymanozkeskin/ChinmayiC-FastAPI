# models.py
from sqlalchemy import create_engine, Column, Integer, String,Float,DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/ChinmayiC"
Base = declarative_base()

# Create the table and establish a connection
def create_table_and_connection():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    return Session()


class Lead(Base):
    __tablename__ = "leads"

    id = Column(String, primary_key=True)
    phone_work = Column(String)
    first_name = Column(String)
    last_name = Column(String)



class BitcoinPrice(Base):
    __tablename__ = "bitcoin_prices"

    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float)
    timestamp = Column(DateTime)

class BitcoinOHLC(Base):
    __tablename__ = "bitcoin_ohlc"

    id = Column(Integer, primary_key=True, autoincrement=True)
    open_price = Column(Float)
    high_price = Column(Float)
    low_price = Column(Float)
    close_price = Column(Float)
    timestamp = Column(DateTime)