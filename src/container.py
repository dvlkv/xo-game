from dependency_injector import containers, providers
from modules import UserModule, GameModule, AuthModule
import sys
import os


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    Users = providers.Singleton(UserModule)
    Auth = providers.Singleton(
        AuthModule,
        users=Users,
        secret=config.auth.secret
    )
    Games = providers.Singleton(GameModule)


Services: Container = Container()


def setup_container() -> Container:
    global Services

    Services.init_resources()
    Services.config.set("db.connection_string", os.getenv("DB_STRING"))
    Services.config.set("auth.secret", os.getenv("AUTH_SECRET"))
    Services.wire(modules=[sys.modules[__name__]])

    return Services
