from cryptography.fernet import Fernet
import os

key_file = "secret.key"

# Generate key if it doesn't exist
def generate_key():
    key = Fernet.generate_key()
    with open(key_file, "wb") as file:
        file.write(key)

# Load encryption key
def load_key():
    if not os.path.exists(key_file):
        generate_key()
    with open(key_file, "rb") as file:
        return file.read()

# Encrypt and decrypt
fernet = Fernet(load_key())

def encrypt(data):
    return fernet.encrypt(data.encode()).decode()

def decrypt(token):
    return fernet.decrypt(token.encode()).decode()
