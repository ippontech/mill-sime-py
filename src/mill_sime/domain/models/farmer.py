from dataclasses import dataclass, field
from uuid import uuid4


class FarmerReference(str):
    """Farmer id"""

    @classmethod
    def create(cls) -> "FarmerReference":
        return cls(uuid4())


@dataclass(kw_only=True)
class Farmer:
    reference: FarmerReference = field(default_factory=FarmerReference.create)
    first_name: str
    last_name: str
    email: str
    phone_number: str
