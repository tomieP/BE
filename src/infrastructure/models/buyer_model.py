from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from .user_model import UserModel

class BuyerModel(UserModel):
    __tablename__ = 'appraiser'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, ForeignKey('flask_user.id'), primary_key=True)
    address = Column(String(50), nullable=False)
    
    __mapper_args__ = {
    'polymorphic_identity': 'buyer',
}