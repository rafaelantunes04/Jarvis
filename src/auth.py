from fastapi import HTTPException, status, Cookie
import re
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
import os
import jwt
from datetime import datetime, timezone, timedelta
import secrets

class Authenticator:
    def __init__(self):
        self.hasher = PasswordHasher()

        self.secret_key = secrets.token_hex(32)

        if not os.getenv("APP_PASSWORD"):
            print("WARNING: Password not set in .ENV")
            return

        # Hash Password in env if not hashed
        if not self.is_argon2_hash(os.getenv("APP_PASSWORD")):
            os.environ["APP_PASSWORD"] = self.hasher.hash(os.getenv("APP_PASSWORD"))

    def is_argon2_hash(self, password_str: str) -> bool:
        """
        Verifica se a string é um hash Argon2
        """
        return re.match(
            r'^\$argon2(i|d|id)\$v=\d+\$m=\d+,t=\d+,p=\d+\$[a-zA-Z0-9+/]+\$[a-zA-Z0-9+/]+$',
            password_str
        ) is not None

    def verify_login(self, username: str, password: str) -> str:
        """
        Verification of user input from the app
        """
        if username != os.getenv("APP_USERNAME"):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas.",
            )

        try:
            self.hasher.verify(os.getenv("APP_PASSWORD"), password)
        except VerifyMismatchError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciais inválidas.",
            )


        return jwt.encode(
            {"sub": username, "exp": datetime.now(timezone.utc) + timedelta(minutes=30)},
            self.secret_key,
            algorithm="HS256"
        )

    def verify_token(self, token: str = Cookie(None)) -> dict:
        """
        Valida um JWT token e retorna o payload
        """
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