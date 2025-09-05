<<<<<<< HEAD
from sqlalchemy import Column, Integer,ForeignKey, String, DateTime, Boolean
=======
from sqlalchemy import Column, Integer,ForeignKey, String, DateTime, Boolean, Float
>>>>>>> d635e6eddb3c41f0ece5b0bc53cc03fd74c740bc
from infrastructure.databases.base import Base

class TrasnactionModel(Base):
    __tablename__ = 'transaction'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    watchid = Column(Integer,ForeignKey('watch.id'))
    sellerid = Column(Integer,ForeignKey('seller.id'))
    buyerid = Column(Integer,ForeignKey('buyer.id'))
    date = Column(DateTime)
<<<<<<< HEAD
    price = Column(float)
=======
    price = Column(Float)
>>>>>>> d635e6eddb3c41f0ece5b0bc53cc03fd74c740bc
    status = Column(Boolean,nullable=False)