from dependency_injector import containers, providers
from app.authentication.persistence.memory.token_service import TokenMemoryPersistenceService
from app.authentication.persistence.redis.token import TokenRedisPersistenceService

class TokenPersistences(containers.DeclarativeContainer):
    memory = providers.Singleton(
        TokenMemoryPersistenceService
    )

    redis = providers.Singleton(
        TokenRedisPersistenceService
    )

    carlemany = redis
