import yaml
import os
from utils.decryption_utils import DecryptText
from dotenv import load_dotenv


class ConfigLoader:

    @staticmethod
    def load_config():
        with open("utils/config/config.yaml") as f:
            data = yaml.safe_load(f)

        load_dotenv(override=True)
        encryption_key = os.getenv("KEY")

        if encryption_key is None:
            raise Exception("Encryption key is not found!")
        decrypted_text = DecryptText.decrypt(
            data["encrypted_password"], encryption_key
        )

        data["PASSWORD"] = decrypted_text
        return data
