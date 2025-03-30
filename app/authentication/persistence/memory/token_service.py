import uuid
from typing import Optional
from app.authentication.domain.persistences.token_interface import TokenInterface


class TokenMemoryPersistenceService(TokenInterface):
    def __init__(self):
        self.tokens = {}

    async def create_token(self, username: str) -> str:
        token = str(uuid.uuid4())
        while token in self.tokens:
            token = str(uuid.uuid4())
        self.tokens[token] = username
        return token

    async def introspect_token(self, token: str) -> Optional[str]:
        return self.tokens.get(token)

    async def delete_token(self, token: str) -> None:
        if token in self.tokens:
            del self.tokens[token]
