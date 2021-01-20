from dependency_injector import containers, providers
from modules import UserModule, GameModule, AuthModule
import sys


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    Users = providers.Singleton(UserModule)
    Auth = providers.Singleton(
        AuthModule,
        users=Users
    )
    Games = providers.Singleton(GameModule)


Services: Container = Container()


def setup_container() -> Container:
    global Services

    Services.init_resources()
    Services.config.set("db.connection_string", "postgresql+asyncpg://postgres:postgres@localhost/XOGame")
    Services.wire(modules=[sys.modules[__name__]])

    return Services
