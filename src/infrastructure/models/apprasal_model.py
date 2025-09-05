<<<<<<< HEAD
from sqlalchemy import Column, Integer,ForeignKey, String, DateTime, Boolean
=======
from sqlalchemy import Column, Integer,ForeignKey, String, DateTime, Boolean,Float
>>>>>>> d635e6eddb3c41f0ece5b0bc53cc03fd74c740bc
from infrastructure.databases.base import Base

class AppraisalModel(Base):
    __tablename__ = 'appraisal'
    __table_args__ = {'extend_existing': True}  # Thêm dòng này

    id = Column(Integer, primary_key=True)
    watchid = Column(Integer,ForeignKey('watch.id'))
    appraiserid = Column(Integer,ForeignKey('appraiser.id'))
<<<<<<< HEAD
    value_estimate = Column(float,nullable= False)
=======
    value_estimate = Column(Float,nullable= False)
>>>>>>> d635e6eddb3c41f0ece5b0bc53cc03fd74c740bc
    condition_note = Column(String(100),nullable=False)
    authenticated = Column(Boolean,nullable= False)
    created_at = Column(DateTime)
