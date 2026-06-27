from fastapi import HTTPException, status
from pydantic import BaseModel
import os


class LoginRequest(BaseModel):
    username: str
    password: str


def verify_credentials(data: LoginRequest) -> str:
    expected_user = os.getenv("APP_USERNAME")
    expected_pass = os.getenv("APP_PASSWORD")
    if data.username != expected_user or data.password != expected_pass:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais inválidas.",
        )
    return data.username