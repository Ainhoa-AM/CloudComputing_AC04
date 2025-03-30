import uuid
import redis.asyncio as redis
from typing import Optional
from app.authentication.domain.persistences.token_interface import TokenInterface


class TokenRedisPersistenceService(TokenInterface):
    def __init__(self, redis_host: str = "redis", redis_port: int = 6379):
        self.redis_instance = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)

    async def create_token(self, username: str) -> str:
        random_id = str(uuid.uuid4())

        while await self.redis_instance.exists(random_id):
            random_id = str(uuid.uuid4())

        await self.redis_instance.set(random_id, username, ex=3600)
        return random_id

    async def introspect_token(self, token: str) -> str | None:
        user = await self.redis_instance.get(token)

        if not user:
            return None
        return user

    async def delete_token(self, token: str) -> None:
        await self.redis_instance.delete(token)
