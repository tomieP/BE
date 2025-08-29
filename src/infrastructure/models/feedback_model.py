from sqlalchemy import Column, Integer,ForeignKey, String, DateTime, Boolean
from infrastructure.databases.base import Base

class FeedbackModel(Base):
    __tablename__ = 'feedback'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    from_userid = Column(Integer,ForeignKey('flask_user.id'))
    to_userid = Column(Integer,ForeignKey('flask_user.id'))
    rating = Column(Integer,nullable=False)
    comment = Column(String(100),nullable=True)
    created_at = Column(DateTime)
