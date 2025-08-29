from sqlalchemy import Column, Integer, String,ForeignKey, DateTime, Boolean
from infrastructure.databases.base import Base

class WatchModel(Base):
    __tablename__ = 'watch'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    sellerid = Column(Integer,ForeignKey('seller.id'))
    name = Column(String(18), nullable=False)
    brand = Column(String(18),nullable= False)
    description = Column(String(500), nullable=True)
    status = Column(Boolean, nullable=False)
    year = Column(DateTime)