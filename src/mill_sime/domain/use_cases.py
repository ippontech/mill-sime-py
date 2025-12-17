from mill_sime.domain.exceptions import FarmerAlreadyExistsError, FarmerNotFoundError
from mill_sime.domain.models.farmer import Farmer, FarmerReference
from mill_sime.domain.ports.farmer_repository import FarmerRepository


def register(*, farmer: Farmer, farmer_repository: FarmerRepository) -> FarmerReference:
    if farmer_repository.exists(farmer.email):
        raise FarmerAlreadyExistsError(farmer.email)

    farmer_repository.save(farmer)
    return farmer.reference


def get(*, farmer_id: FarmerReference, farmer_repository: FarmerRepository) -> Farmer:
    return farmer_repository.get_by_reference(farmer_id).or_else_raise(
        FarmerNotFoundError(farmer_id)
    )
