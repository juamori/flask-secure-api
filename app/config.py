import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")  # fallback só para dev
    JWT_ALGORITHM = "HS256"
    SQLALCHEMY_DATABASE_URI = "sqlite:///users.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
