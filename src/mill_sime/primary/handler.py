from http import HTTPStatus
from typing import Any

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import ApiGatewayResolver, Response
from aws_lambda_powertools.logging.correlation_paths import API_GATEWAY_REST
from aws_lambda_powertools.utilities.typing import LambdaContext

from mill_sime.config import setting
from mill_sime.domain.exceptions import AlreadyExistsError, NotFoundError
from mill_sime.primary.common.responses import JSONResponse
from mill_sime.primary.common.serializer import custom_serializer
from mill_sime.primary.common.uri import BASE_API_URI, FARMER_API_URI
from mill_sime.primary.routes import farmer

tracer = Tracer()
logger = Logger(service=setting.project_name)
app = ApiGatewayResolver(strip_prefixes=[BASE_API_URI], serializer=custom_serializer)

app.include_router(router=farmer.router, prefix=FARMER_API_URI)


@app.exception_handler(NotFoundError)
def handle_not_found(exc: NotFoundError) -> Response[dict[str, Any]]:
    return JSONResponse(
        status_code=HTTPStatus.NOT_FOUND,
        body={"message": str(exc)},
    )


@app.exception_handler(AlreadyExistsError)
def handle_already_exists(exc: AlreadyExistsError) -> Response[dict[str, Any]]:
    return JSONResponse(
        status_code=HTTPStatus.CONFLICT,
        body={"message": str(exc)},
    )


@tracer.capture_lambda_handler
@logger.inject_lambda_context(correlation_id_path=API_GATEWAY_REST, log_event=True)
def lambda_handler(event: dict[str, Any], context: LambdaContext) -> dict[str, Any]:
    return app.resolve(event, context)
