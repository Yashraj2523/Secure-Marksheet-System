from flask import Flask, request, jsonify, send_file
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS 
from models import db, User, Document
from utils import encrypt_file, decrypt_file, hash_password, verify_password, hash_file
from sqlalchemy import inspect
from functools import wraps
from flask_jwt_extended import get_jwt_identity
import io
app = Flask(__name__)
CORS(app)
app.config.from_object('config.Config') 

db.init_app(app)
jwt = JWTManager(app)

with app.app_context():
    db.create_all()

@app.route('/')
def index():

    inspector = inspect(db.engine)
    if not inspector.has_table('user') or not inspector.has_table('document'):
        db.create_all()
    return "Welcome to the Secure Document Portal!"

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data:
        return jsonify({"message": "No data provided or invalid content type. Please use JSON."}), 400

    username = data.get('username')
    password = data.get('password')
    role = data.get('role')  

    if not username or not password or not role:
        return jsonify({"message": "Missing data"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"message": "User already exists"}), 400

    password_hash = hash_password(password)
    new_user = User(username=username, password_hash=password_hash, role=role)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and verify_password(password, user.password_hash):
        access_token = create_access_token(identity={'username': user.username, 'role': user.role})
        return jsonify(access_token=access_token), 200
    return jsonify({"message": "Invalid credentials"}), 401

def role_required(*roles):
    def wrapper(fn):
        @wraps(fn)
        @jwt_required()
        def decorated_function(*args, **kwargs):
            current_user = get_jwt_identity()
            if current_user['role'] not in roles:
                return jsonify({"message": "Access denied: insufficient privileges"}), 403
            return fn(*args, **kwargs)
        return decorated_function
    return wrapper


@app.route('/upload', methods=['POST'])
@role_required('faculty', 'admin')
@jwt_required()
def upload():
    current_user=get_jwt_identity()
    
    if current_user['role'] != 'faculty':
        return jsonify({"message": "Only faculty members are allowed to upload files"}),403
    
    file = request.files['file']
    if not file:
        return jsonify({"message":"No file"}),400
    
    file_data = file.read()
    encrypted_file = encrypt_file(file_data)
    checksum = hash_file(file_data)

    uploader = User.query.filter_by(username=current_user['username']).first()
    new_document = Document(
        owner_id=uploader.id,
        filename=file.filename,
        file_data=encrypted_file,
        checksum=checksum,
        uploader_id=uploader.id
    )

    db.session.add(new_document)
    db.session.commit()

    return jsonify({
        "message": "File uploaded successfully",
        "doc_id": new_document.id  
    }), 201

@app.route('/my-documents', methods=['GET'])
@jwt_required()
def get_my_documents():
    current_user = get_jwt_identity()
    user = User.query.filter_by(username=current_user['username']).first()
    
    documents = Document.query.filter_by(owner_id=user.id).all()
    document_list = [{"id": doc.id, "filename": doc.filename} for doc in documents]

    return jsonify(document_list), 200


@app.route('/download/<int:doc_id>', methods=['GET'])
@jwt_required()
def download(doc_id):
    current_user = get_jwt_identity()
    document = Document.query.filter_by(id=doc_id).first()
    if not document:
        return jsonify({"message": "Document not found"}), 404
    
    uploader = User.query.filter_by(id=document.uploader_id).first()
    if not uploader:
        return jsonify({"message":"Uploader not found"}),404

    user = User.query.filter_by(username=current_user['username']).first()
    if user.role == 'student' and uploader.role != 'faculty':
            return jsonify({"message":"Students can only download documents uploaded by faculty"}),403

    decrypted_file = decrypt_file(document.file_data)

    if hash_file(decrypted_file) != document.checksum:
        return jsonify({"message": "File integrity check failed!"}), 400

    return send_file(
        io.BytesIO(decrypted_file),
        download_name=document.filename,
        as_attachment=True
    )

@app.route('/admin-only', methods=['GET'])
@role_required('admin')
@jwt_required()
def admin_route():
    current_user = get_jwt_identity()

    if current_user['role'] != 'admin':
        return jsonify({"message": "Admins only!"}), 403

    return jsonify({"message": "Welcome, Admin!"})

if __name__ == '__main__':
    app.run(debug=True)