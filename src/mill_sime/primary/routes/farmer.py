from http import HTTPStatus

from fastapi import APIRouter
from fastapi.responses import RedirectResponse

from mill_sime.dependencies import FarmerRepositoryDep
from mill_sime.domain.models.farmer import Farmer, FarmerReference
from mill_sime.domain.use_cases import get, register
from mill_sime.primary.routes.requests.farmer_request import CreateFarmerRequest
from mill_sime.primary.routes.responses.farmer import FarmerOutput

FARMER_BASE_PATH = "/api/farmers"

router = APIRouter(prefix=FARMER_BASE_PATH, tags=["farmers"])


@router.get("/{farmer_id}", response_model=FarmerOutput, status_code=HTTPStatus.OK)
async def get_farmer_by_id(farmer_id: str, farmer_repository: FarmerRepositoryDep) -> Farmer:
    return get(farmer_id=FarmerReference(farmer_id), farmer_repository=farmer_repository)


@router.post(
    "/",
    response_class=RedirectResponse,
    status_code=HTTPStatus.CREATED,
    responses={HTTPStatus.CONFLICT: {"description": "Farmer already exists"}},
)
async def create_farmer(
    new_farmer: CreateFarmerRequest, farmer_repository: FarmerRepositoryDep
) -> RedirectResponse:
    farmer: Farmer = new_farmer.to_domain()
    register(farmer=farmer, farmer_repository=farmer_repository)

    return RedirectResponse(
        status_code=HTTPStatus.CREATED,
        url=f"{FARMER_BASE_PATH}/{farmer.reference}",
    )
