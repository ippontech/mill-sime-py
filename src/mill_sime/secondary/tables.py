# Classe de base
from sqlmodel import Field, SQLModel

from mill_sime.domain.models.farmer import Farmer, FarmerReference


class FarmerModel(SQLModel, table=True):
    __tablename__ = "farmer"
    id: str = Field(primary_key=True)
    first_name: str = Field(nullable=False)
    last_name: str = Field(nullable=False)
    email: str = Field(nullable=False, unique=True, index=True)
    phone_number: str = Field(nullable=False)

    @classmethod
    def from_domain(cls, farmer: Farmer) -> "FarmerModel":
        return FarmerModel(
            id=farmer.reference,
            first_name=farmer.first_name,
            last_name=farmer.last_name,
            email=farmer.email,
            phone_number=farmer.phone_number,
        )

    def to_domain(self) -> Farmer:
        return Farmer(
            reference=FarmerReference(self.id),
            first_name=self.first_name,
            last_name=self.last_name,
            email=self.email,
            phone_number=self.phone_number,
        )
