from fastapi import HTTPException, status
from os import getenv


def verify_credentials(username: str, password: str) -> str:
    """
    Verification of user input from the app
    """
    expected_user = getenv("APP_USERNAME")
    expected_pass = getenv("APP_PASSWORD")
    if username != expected_user or password != expected_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )
    return username