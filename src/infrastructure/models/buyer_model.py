from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from .user_model import UserModel

class BuyerModel(UserModel):
    __tablename__ = 'buyer'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, ForeignKey('flask_user.id'), primary_key=True)
    address = Column(String(100), nullable=False)
    
    __mapper_args__ = {
    'polymorphic_identity': 'buyer',
}