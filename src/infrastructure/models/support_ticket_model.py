from sqlalchemy import Column, Integer,ForeignKey, String, DateTime, Boolean
from infrastructure.databases.base import Base

class Support_TicketModel(Base):
    __tablename__ = 'support_ticket'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    support_agentid = Column(Integer,ForeignKey('support_agent.id'))
    userid = Column(Integer,ForeignKey('flask_user.id'))
    msg = Column(String(255),nullable=False)
    status = Column(Boolean, nullable=False)
    created_at = Column(DateTime)
    updated_at = Column(DateTime) 