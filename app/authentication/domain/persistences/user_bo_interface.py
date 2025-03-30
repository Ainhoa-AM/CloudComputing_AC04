from abc import ABC, abstractmethod
from app.authentication.domain.bo.user_bo import UserBO

class UserBOInterface(ABC):

    @abstractmethod
    def create_user(self, user: UserBO):
        pass

    @abstractmethod
    def get_user(self, username: str):
        pass

