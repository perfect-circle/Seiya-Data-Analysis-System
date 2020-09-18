from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql://root:123456@47.104.245.220:3306/seiya')
Base = declarative_base()
Session = sessionmaker(bind=engine)
