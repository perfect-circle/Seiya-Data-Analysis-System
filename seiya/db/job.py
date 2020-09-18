from sqlalchemy import Column, String, Integer

from seiya.db.base import Base

class JobModel(Base):
    """职业 Model
    """
    __tablename__ = 'job'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(64))
    city = Column(String(16))
    salary_lower = Column(Integer)
    salary_upper = Column(Integer)
    experience_lower = Column(Integer)
    experience_upper = Column(Integer)
    edeucation = Column(String(16))
    tags = Column(String(256))
    company = Column(String(32))
