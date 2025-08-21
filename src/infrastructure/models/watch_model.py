from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean
from sqlalchemy.sql import func
from infrastructure.databases.database import db

class WatchModel(db.Model):
    __tablename__ = 'watch'

    id = Column(Integer, primary_key=True, autoincrement=True)
    seller_id = Column(Integer, ForeignKey('seller.id'), nullable=False)
    model = Column(String(18), nullable=False)
    brand = Column(String(18), nullable=False)
    description = Column(String(255), nullable=True)
    condition = Column(String(50), nullable=True)
    appraisal_status = Column(String(50), nullable=False, default='pending')
    year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    def __repr__(self):
        return f"<WatchModel(id={self.id}, model={self.model}, brand={self.brand})>"