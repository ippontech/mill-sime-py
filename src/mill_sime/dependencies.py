from typing import Annotated

from fastapi import Depends
from sqlalchemy import Engine, create_engine

from mill_sime.config import setting
from mill_sime.domain.ports.farmer_repository import FarmerRepository
from mill_sime.secondary.farmer_repository import SqlAlchemyFarmerRepository


def get_engine() -> Engine:
    return create_engine(setting.db_url)


def get_farmer_repository(engine: Annotated[Engine, Depends(get_engine)]) -> FarmerRepository:
    return SqlAlchemyFarmerRepository(engine)


FarmerRepositoryDep = Annotated[FarmerRepository, Depends(get_farmer_repository)]
