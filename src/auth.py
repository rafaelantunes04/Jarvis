from fastapi import HTTPException, status
import os


def verify_credentials(username: str, password: str) -> str:
    expected_user = os.getenv("APP_USERNAME")
    expected_pass = os.getenv("APP_PASSWORD")
    if username != expected_user or password != expected_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )
    return username