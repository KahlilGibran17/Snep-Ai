from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

url = URL.create(
    drivername="postgresql",
    username='snepai',
    password='********',
    host='ep-tight-hat-a4gipbbj.us-east-1.pg.koyeb.app',
    database='information_validation_news',
)

engine = create_engine(url)

session = Session(engine)
