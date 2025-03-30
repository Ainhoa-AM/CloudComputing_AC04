from dependency_injector import containers, providers
from app.authentication.persistence.memory.user_bo import UserBOMemoryPersistenceService
from app.authentication.domain.controllers.login_controller import LoginController


class LoginControllers(containers.DeclarativeContainer):
    carlemany = providers.Singleton(
        LoginController,
        user_persistence_service=UserBOMemoryPersistenceService()
    )


login_controllers = LoginControllers()
login_controller = login_controllers.carlemany()
