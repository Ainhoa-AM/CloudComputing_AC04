from app.authentication.domain.bo.user_bo import UserBO
from hashlib import sha256
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface

class RegisterController:
    def __init__(self, user_persistence_service: UserBOInterface):
        self.user_persistence_service = user_persistence_service

    async def __call__(self, username: str, password: str, mail: str, year_of_birth: int):
        hash_password = username + password
        hashed_password = str(sha256(hash_password.encode()).digest().hex())

        new_user = UserBO(
            username=username,
            password=hashed_password,
            mail=mail,
            year_of_birth=year_of_birth,
        )

        await self.user_persistence_service.create_user(user=new_user)

        return new_user

