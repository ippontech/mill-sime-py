import json
from typing import Any

from pydantic import BaseModel


def custom_serializer(obj: Any) -> str:
    """
    Custom serializer that forces Pydantic models to dump by alias (camelCase).
    """

    def default_handler(o: Any) -> Any:
        if isinstance(o, BaseModel):
            return o.model_dump(by_alias=True)
        return str(o)

    return json.dumps(obj, default=default_handler)
