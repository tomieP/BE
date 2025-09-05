<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
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

class SellerModel(db.Model):
    __tablename__ = 'seller'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

class SupportTicket(db.Model):
    __tablename__ = 'support_tickets'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, default='open')
    assigned_to = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, autoincrement=True)
    ticket_id = Column(Integer, ForeignKey('support_tickets.id'), nullable=True)
    customer_id = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
=======
from sqlalchemy import Column, Integer, String,ForeignKey, DateTime, Boolean
from infrastructure.databases.base import Base

class WatchModel(Base):
    __tablename__ = 'watch'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    sellerid = Column(Integer,ForeignKey('seller.id'))
    name = Column(String(18), nullable=False)
    brand = Column(String(18),nullable= False)
    description = Column(String(500), nullable=True)
    status = Column(Boolean, nullable=False)
    year = Column(DateTime)
>>>>>>> d635e6eddb3c41f0ece5b0bc53cc03fd74c740bc
