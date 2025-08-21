import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "mssql+pyodbc://sa:Aa123456@localhost:1433/watch_appraisal?driver=ODBC+Driver+17+for+SQL+Server")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = Config()