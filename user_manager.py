import hashlib
from typing import Optional, Tuple
from database import Database


class UserManager:
    def __init__(self, database: Database):
        self.db = database

    def register_user(self, username: str, password: str, user_type: str) -> bool:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        return self.db.add_user(username, hashed_password, user_type)

    def authenticate_user(
        self, username: str, password: str
    ) -> Tuple[bool, Optional[str]]:
        user = self.db.get_user(username)
        if user:
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if user[1] == hashed_password:
                return True, user[2]
        return False, None
