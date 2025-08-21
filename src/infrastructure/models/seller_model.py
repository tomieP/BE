from sqlalchemy import Column, Integer, String
from infrastructure.databases.database import db

class SellerModel(db.Model):
    __tablename__ = 'seller'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)