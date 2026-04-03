from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Singleton
from sqlalchemy import create_engine

from mill_sime import primary
from mill_sime.config import setting
from mill_sime.domain.ports.farmer_repository import FarmerRepository
from mill_sime.secondary.farmer_repository import SqlAlchemyFarmerRepository


class Container(DeclarativeContainer):
    engine = Singleton(create_engine, setting.db_url)
    farmer_repository: Singleton[FarmerRepository] = Singleton(SqlAlchemyFarmerRepository, engine)


container = Container()
container.wire(packages=[primary])
