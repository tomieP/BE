from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from .user_model import UserModel

class BuyerModel(UserModel):
<<<<<<< HEAD
    __tablename__ = 'appraiser'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, ForeignKey('flask_user.id'), primary_key=True)
    address = Column(String(50), nullable=False)
=======
    __tablename__ = 'buyer'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, ForeignKey('flask_user.id'), primary_key=True)
    address = Column(String(100), nullable=False)
>>>>>>> d635e6eddb3c41f0ece5b0bc53cc03fd74c740bc
    
    __mapper_args__ = {
    'polymorphic_identity': 'buyer',
}