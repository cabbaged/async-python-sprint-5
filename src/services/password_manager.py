from fastapi import Header, HTTPException
from jose import JWTError, jwt
from passlib.context import CryptContext


class PasswordManager:
    @classmethod
    def create(cls):
        return PasswordManager()

    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    def hash_password(self, password):
        return self.pwd_context.hash(password)

    def create_access_token(self, data: dict):
        to_encode = data.copy()
        return jwt.encode(to_encode, "secret", algorithm="HS256")

    @staticmethod
    def get_current_user(token: str = Header(...)):
        try:
            payload = jwt.decode(token, "secret", algorithms=["HS256"])
            username: str = payload.get("sub")
            if not username:
                raise HTTPException(status_code=401, detail="Could not validate credentials")
            return username
        except JWTError:
            raise HTTPException(status_code=401, detail="Could not validate credentials")
