import yaml
import os
from utils.encryption_utils import decrypt_text
from dotenv import load_dotenv


def load_config():
    with open("config/config.yaml") as f:
        data = yaml.safe_load(f)

    load_dotenv(override=True)
    encryption_key = os.getenv("KEY")

    if encryption_key is None:
        raise Exception("Encryption key is not found!")
    decrypted_text = decrypt_text(
        data["encrypted_password"], encryption_key
    )

    data["PASSWORD"] = decrypted_text
    return data
