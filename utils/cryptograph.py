from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

import json
import base64

from datetime import date, datetime, time



def derive_key(password, salt):
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
    )
    
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return key

def encrypt_and_write(data, file_path, password, salt):
    key = derive_key(password, salt)
    f = Fernet(key)
    json_bytes = json.dumps(data, indent=4, default=default_serializer).encode()
    encrypted = f.encrypt(json_bytes)
    with open(file_path, "wb") as file:
        file.write(encrypted)

def read_and_decrypt(file_path, password, salt):
    key = derive_key(password, salt)
    f = Fernet(key)
    with open(file_path, "rb") as file:
        encrypted = file.read()
    decrypted = f.decrypt(encrypted)
    return json.loads(decrypted.decode())

def default_serializer(obj):
    if isinstance(obj, (datetime, date, time)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")