from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), nullable=False)  

class Document(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(200), nullable=False)
    file_data = db.Column(db.LargeBinary, nullable=False)  
    checksum = db.Column(db.String(64), nullable=False)  
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  
