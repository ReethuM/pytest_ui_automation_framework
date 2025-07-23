from cryptography.fernet import Fernet


def generate_key():
    """Generate a secure encryption key"""
    key = Fernet.generate_key()
    return key.decode()


def encrypt_text(plain_text, key):
    """Encrypt any plain text using the provided key"""
    try:
        fernet = Fernet(key.encode())
        encrypted_text = fernet.encrypt(plain_text.encode())
        return encrypted_text.decode()
    except Exception as e:
        raise ValueError(f"Encryption failed: {e}")


def decrypt_text(encrypted_text, key):
    """Decrypt encrypted text using the provided key"""
    try:
        fernet = Fernet(key.encode())
        return fernet.decrypt(encrypted_text.encode()).decode()
    except Exception as e:
        raise ValueError(f"Decryption failed: {e}")
