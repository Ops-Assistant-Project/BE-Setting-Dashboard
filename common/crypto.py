import os
from dotenv import load_dotenv
from cryptography.fernet import Fernet

load_dotenv()

FERNET_KEY = os.getenv("FERNET_KEY")
if not FERNET_KEY:
    raise RuntimeError("FERNET_KEY is not set")

_fernet = Fernet(FERNET_KEY.encode())


def encrypt(value: str) -> str:
    """
    문자열 암호화 (저장용)
    """
    return _fernet.encrypt(value.encode()).decode()


def decrypt(value: str) -> str:
    """
    문자열 복호화 (사용 시)
    """
    return _fernet.decrypt(value.encode()).decode()
