from http import HTTPStatus
from typing import Annotated

from aws_lambda_powertools.event_handler.api_gateway import Router
from dependency_injector.wiring import Provide, inject

from mill_sime.dependencies import Container
from mill_sime.domain.models.farmer import Farmer, FarmerReference
from mill_sime.domain.ports.farmer_repository import FarmerRepository
from mill_sime.domain.use_cases import get, register
from mill_sime.primary.common.responses import JSONResponse
from mill_sime.primary.common.uri import BASE_API_URI, FARMER_API_URI
from mill_sime.primary.routes.requests.farmer_request import CreateFarmerRequest
from mill_sime.primary.routes.responses.farmer import FarmerOutput

FarmerRepositoryDep = Annotated[FarmerRepository, Provide[Container.farmer_repository]]
router = Router()  # type: ignore[no-untyped-call]


@router.get("/<farmer_id>")
@inject
def get_farmer_by_id(
    farmer_id: str, farmer_repository: FarmerRepositoryDep
) -> JSONResponse[FarmerOutput]:
    return JSONResponse(
        status_code=HTTPStatus.OK,
        body=FarmerOutput.model_validate(
            get(farmer_id=FarmerReference(farmer_id), farmer_repository=farmer_repository)
        ),
    )


@router.post("/")
@inject
def create_farmer(farmer_repository: FarmerRepositoryDep) -> JSONResponse[None]:
    body = CreateFarmerRequest.model_validate(router.current_event.json_body)
    farmer: Farmer = body.to_domain()
    register(farmer=farmer, farmer_repository=farmer_repository)

    return JSONResponse(
        status_code=HTTPStatus.CREATED,
        headers={"Location": f"{BASE_API_URI}{FARMER_API_URI}/{farmer.reference}"},
    )
