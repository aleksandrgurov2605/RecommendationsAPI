from pwdlib import PasswordHash

# Инициализация с рекомендуемыми настройками (по умолчанию Argon2)
password_hash = PasswordHash.recommended()

def get_password_hash(password: str) -> str:
    """
    Хеширование пароля.
    :param password:
    :return:
    """
    return password_hash.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверка соответствия пароля хешу
    :param plain_password:
    :param hashed_password:
    :return:
    """
    return password_hash.verify(plain_password, hashed_password)