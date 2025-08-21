from sqlalchemy import Column, Integer, String, DateTime, Boolean,ForeignKey
from .user_model import UserModel

class AdministratorModel(UserModel):
    __tablename__ = 'administrator'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, ForeignKey('flask_user.id'), primary_key=True)

    __mapper_args__ = {
    'polymorphic_identity': 'administrator',
    }