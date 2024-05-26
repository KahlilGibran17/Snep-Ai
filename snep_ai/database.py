from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session

class Base(DeclarativeBase):
    pass

url = URL.create(
    drivername="postgresql",
    username='lsffsezngtsopp',
    password='479c2473c4a74232723b00658bd5263312d8cf813933770056591d5007d44dc0',
    host='ec2-18-235-117-73.compute-1.amazonaws.com',
    database='dbj3tq4jjfh1ci',
)

engine = create_engine(url)

session = Session(engine)
