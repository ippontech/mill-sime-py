from collections.abc import Mapping

from aws_lambda_powertools.event_handler import Response
from aws_lambda_powertools.event_handler.content_types import APPLICATION_JSON


class JSONResponse[T](Response[T]):
    def __init__(
        self,
        status_code: int,
        body: T | None = None,
        headers: Mapping[str, str | list[str]] | None = None,
    ) -> None:
        super().__init__(
            status_code=status_code, body=body, headers=headers, content_type=APPLICATION_JSON
        )
