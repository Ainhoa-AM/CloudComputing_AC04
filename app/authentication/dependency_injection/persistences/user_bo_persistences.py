from dependency_injector import containers, providers
from app.authentication.persistence.memory.user_bo import UserBOMemoryPersistenceService
from app.authentication.persistence.postgres.user_bo import UserBOPostgresPersistenceService


class UserBOPersistences(containers.DeclarativeContainer):
    memory = providers.Singleton(
        UserBOMemoryPersistenceService
    )
    postgres = providers.Singleton(
        UserBOPostgresPersistenceService
    )
    carlemany = postgres
