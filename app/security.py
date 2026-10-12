from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from jwt import encode
from pwdlib import PasswordHash

from app.settings import Settings

load_dotenv()

password_hash = PasswordHash.recommended()
settings = Settings()


def get_hash(password: str) -> str:
    return password_hash.hash(password=password)


def verify_hash_password(plain_password: str, hash_password: str) -> bool:
    return password_hash.verify(password=plain_password, hash=hash_password)


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now(tz=ZoneInfo('UTC')) + timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire})

    # Header é criado com key de 'JWT' por trás
    token = encode(
        payload=to_encode,
        key=settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )

    return token


def main():
    data: dict = {'sub': 'caio@email.com'}
    create_access_token(data=data)


if __name__ == '__main__':
    main()
