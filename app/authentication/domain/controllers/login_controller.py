import uuid
from hashlib import sha256
from app.authentication.domain.persistences.exceptions import WrongPasswordException
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface


class LoginController:
    def __init__(self, user_persistence_service: UserBOInterface):
        self.user_persistence_service = user_persistence_service
        self.tokens = {}

    async def __call__(self, username: str, password: str) -> str:
        stored_user = await self.user_persistence_service.get_user(username=username)
        hashed_stored_password = stored_user.password

        hash_password = username + password
        hashed_input_password = str(sha256(hash_password.encode()).digest().hex())

        if hashed_stored_password == hashed_input_password:
            random_id = str(uuid.uuid4())
            while random_id in self.tokens:
                random_id = str(uuid.uuid4())
            self.tokens[random_id] = username
            return random_id
        else:
            raise WrongPasswordException()



