import os

class Config:
    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_URI_TEST = os.getenv("MONGO_URI_TEST", "mongodb://localhost:27017")
    JWT_SECRET = os.getenv("JWT_SECRET", "mock_secret")  # Mock JWT secret for testing

config = Config()