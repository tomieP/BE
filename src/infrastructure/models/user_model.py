from sqlalchemy import Column, Integer, String, DateTime, Boolean
from infrastructure.databases.base import Base

class UserModel(Base):
    __tablename__ = 'flask_user'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    user_name = Column(String(18), nullable=False)
    password = Column(String(18), nullable=False)
    email = Column(String(50),nullable= False)
    description = Column(String(255), nullable=True)
    status = Column(Boolean, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime) 

    type = Column(String(50))  # dùng để phân biệt subtype
    __mapper_args__ ={
        'polymorphic_identity': 'user',
        'polymorphic_on': type
    }