class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///documents.db'  
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_secret_key'  
