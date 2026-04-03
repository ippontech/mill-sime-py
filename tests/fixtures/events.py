import json
from dataclasses import dataclass
from http import HTTPMethod
from typing import Any

from aws_lambda_powertools.utilities.typing import LambdaContext


def create_api_call(
    path: str, method: HTTPMethod, body: dict[Any, Any] | None = None
) -> tuple[dict[str, Any], LambdaContext]:
    return {
        "resource": path,
        "path": path,
        "httpMethod": method.value,
        "headers": {"Accept": "application/json", "content-type": "application/json"},
        "body": json.dumps(body if body else {}),
    }, lambda_context()


def lambda_context() -> LambdaContext:
    @dataclass
    class Context(LambdaContext):
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = "arn:aws:lambda:eu-west-1:123456789012:function:test"
        aws_request_id: str = "da658bd3-2d6f-4e7b-8ec2-937234644fdc"

    return Context()
