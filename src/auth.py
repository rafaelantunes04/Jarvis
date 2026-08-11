from fastapi import HTTPException, status, Cookie
import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os
import jwt
from datetime import datetime, timezone, timedelta
import secrets

from src.config import MAX_ATTEMPTS, WINDOW_SECONDS

class Authenticator:
    def __init__(self):
        self.hasher = PasswordHasher()
        self.secret_key = secrets.token_hex(32)
        self.last_attempts = 0
        self.last_attempt_time = datetime.now(timezone.utc)

        # Hash password if not already hashed
        if not self.is_argon2_hash(os.getenv("APP_PASSWORD")):
            self._hashed_password = self.hasher.hash(os.getenv("APP_PASSWORD"))
        else:
            self._hashed_password = os.getenv("APP_PASSWORD")

    def is_argon2_hash(self, password_str: str) -> bool:
        return re.match(
            r'^\$argon2(i|d|id)\$v=\d+\$m=\d+,t=\d+,p=\d+\$[a-zA-Z0-9+/]+\$[a-zA-Z0-9+/]+$',
            password_str
        ) is not None

    def verify_login(self, username: str, password: str) -> str:
        now = datetime.now(timezone.utc)

        if self.last_attempts >= MAX_ATTEMPTS:
            time_since_last_attempt = now - self.last_attempt_time
            if time_since_last_attempt <= timedelta(seconds=WINDOW_SECONDS):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Máximo de tentativas excedido. Tente novamente mais tarde.",
                )
            self.last_attempts = 0

        self.last_attempts += 1
        self.last_attempt_time = now

        if username != os.getenv("APP_USERNAME"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas.",
            )

        try:
            self.hasher.verify(self._hashed_password, password)
        except VerifyMismatchError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas.",
            )

        self.last_attempts = 0
        return jwt.encode(
            {"sub": username, "exp": now + timedelta(minutes=30)},
            self.secret_key,
            algorithm="HS256"
        )

    def verify_token(self, token: str | None = None) -> dict:
        if not token:
            raise HTTPException(status_code=401, detail="Não autenticado.")
        try:
            return jwt.decode(token, self.secret_key, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expirado.",
                headers={"WWW-Authenticate": "Bearer"},
            )
        except jwt.InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token inválido.",
                headers={"WWW-Authenticate": "Bearer"},
            )

authenticator = Authenticator()