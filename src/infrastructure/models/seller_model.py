<<<<<<< HEAD
from sqlalchemy import Column, Integer, String
from infrastructure.databases.database import db

class SellerModel(db.Model):
    __tablename__ = 'seller'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
=======
from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from .user_model import UserModel

class SellerModel(UserModel):
    __tablename__ = 'seller'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, ForeignKey('flask_user.id'), primary_key=True)

    __mapper_args__ = {
    'polymorphic_identity': 'seller',
}
>>>>>>> d635e6eddb3c41f0ece5b0bc53cc03fd74c740bc
