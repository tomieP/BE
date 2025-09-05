<<<<<<< HEAD
from flask_sqlalchemy import SQLAlchemy
from src.config import Config

db = SQLAlchemy()

def init_mssql(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = Config.SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = Config.SQLALCHEMY_TRACK_MODIFICATIONS
    db.init_app(app)
    with app.app_context():
        db.create_all()
=======
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import Config
from infrastructure.databases.base import Base

# Database configuration
DATABASE_URI = Config.DATABASE_URI
engine = create_engine(DATABASE_URI)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
session = SessionLocal()
def init_mssql(app):
    Base.metadata.create_all(bind=engine)
>>>>>>> d635e6eddb3c41f0ece5b0bc53cc03fd74c740bc
