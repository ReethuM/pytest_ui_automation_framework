from cryptography.fernet import Fernet


class DecryptText:

    @staticmethod
    def decrypt(encrypted_text, key):
        """Decrypt an encrypted text using the provided key"""
        try:
            fernet = Fernet(key.encode())
            return fernet.decrypt(encrypted_text.encode()).decode()
        except Exception as e:
            raise ValueError(f"Decryption failed: {e}")
