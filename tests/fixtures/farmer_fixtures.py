from maypy import maybe

from mill_sime.domain.models.farmer import Farmer, FarmerReference


def create_farmer(
    *,
    reference: str | None = "00000001",
    first_name: str = "Jean",
    last_name: str = "Dupont",
    email: str = "jean.dupont@fermier.fr",
    phone_number: str = "+33 123456789",
) -> Farmer:
    return Farmer(
        reference=maybe(reference).map(FarmerReference).or_else(FarmerReference.create()),
        first_name=first_name,
        last_name=last_name,
        email=email,
        phone_number=phone_number,
    )
