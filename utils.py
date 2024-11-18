import hashlib
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

def encrypt_file(file_data):
    return cipher.encrypt(file_data)

def decrypt_file(encrypted_data):
    return cipher.decrypt(encrypted_data)

def hash_password(password):
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def verify_password(plain_password, hashed_password):
    return hash_password(plain_password) == hashed_password

def hash_file(file_data):
    return hashlib.sha256(file_data).hexdigest()
