from sqlalchemy import Column, Integer,ForeignKey, String, DateTime, Boolean
from infrastructure.databases.base import Base

class ListingModel(Base):
    __tablename__ = 'listing'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    watchid = Column(Integer,ForeignKey('watch.id'))
    sellerid = Column(Integer,ForeignKey('seller.id'))
    buyerid = Column(Integer,ForeignKey('buyer.id'))
    appraisalid = Column(Integer,ForeignKey('appraisal.id'))
    created_at = Column(DateTime)
    price = Column(float)
    status = Column(Boolean,nullable=False)