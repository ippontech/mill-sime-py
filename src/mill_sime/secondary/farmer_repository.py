from typing import override

from maypy import Maybe, maybe
from sqlalchemy import Engine
from sqlmodel import Session, select

from mill_sime.domain.models.farmer import Farmer, FarmerReference
from mill_sime.domain.ports.farmer_repository import FarmerRepository
from mill_sime.secondary.tables import FarmerModel


class SqlAlchemyFarmerRepository(FarmerRepository):
    def __init__(self, engine: Engine) -> None:
        self.engine = engine

    @override
    def get_by_reference(self, reference: FarmerReference) -> Maybe[Farmer]:
        with Session(self.engine) as session:
            statement = select(FarmerModel).where(FarmerModel.id == reference)
            result = session.exec(statement).one_or_none()
            return maybe(result).map(FarmerModel.to_domain)

    @override
    def save(self, farmer: Farmer) -> None:
        with Session(self.engine) as session:
            farmer_entity = FarmerModel.from_domain(farmer)
            session.add(farmer_entity)
            session.commit()
            session.refresh(farmer_entity)

    @override
    def exists(self, email: str) -> bool:
        with Session(self.engine) as session:
            statement = select(FarmerModel.id).where(FarmerModel.email == email)
            result = session.exec(statement).first()
            return result is not None
