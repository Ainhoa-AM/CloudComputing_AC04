from app.authentication.domain.bo.user_bo import UserBO
from app.authentication.domain.persistences.exceptions import UserNotFoundException, UsernameAlreadyTakenException
from app.authentication.domain.persistences.user_bo_interface import UserBOInterface
from app.authentication.domain.models import UserBO
from app.authentication.domain.persistences.exceptions import UsernameAlreadyTakenException, UserNotFoundException

class UserBOMemoryPersistenceService(UserBOInterface):
    def __init__(self):
        self.users = {}

    async def create_user(self, user: UserBO):
        if user.username in self.users:
            raise UsernameAlreadyTakenException
        self.users[user.username] = user

    async def get_user(self, username: str):
        if username not in self.users:
            raise UserNotFoundException
        return self.users[username]



