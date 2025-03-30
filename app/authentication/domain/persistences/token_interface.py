from typing import Optional

class TokenInterface:
    async def create_token(self, username: str) -> str:
        raise NotImplementedError

    async def introspect_token(self, token: str) -> Optional[str]:
        raise NotImplementedError

    async def delete_token(self, token: str) -> None:
        raise NotImplementedError
