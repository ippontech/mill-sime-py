import json
from collections.abc import Iterator
from http import HTTPMethod, HTTPStatus

import pytest
from tests.fixtures.db import get_sqlite_engine
from tests.fixtures.events import create_api_call

from mill_sime.dependencies import container
from mill_sime.primary.common.uri import BASE_API_URI, FARMER_API_URI
from mill_sime.primary.handler import lambda_handler

FARMER_BASE_PATH = f"{BASE_API_URI}{FARMER_API_URI}"


class TestFarmerResource:
    @pytest.fixture(autouse=True)
    def setup(self) -> Iterator[None]:
        with (
            get_sqlite_engine() as engine,
        ):
            container.engine.override(engine)

            yield
            container.engine.reset_override()
            # Reset singletons, otherwise the closed connection will be reused.
            container.reset_singletons()

    def test_create_new_farm(self) -> None:
        request = {
            "email": "jean.dupont@fermier.fr",
            "firstName": "Jean",
            "lastName": "Dupont",
            "phoneNumber": "+33 123456789",
        }
        response = lambda_handler(*create_api_call(FARMER_BASE_PATH, HTTPMethod.POST, body=request))

        assert response["statusCode"] == HTTPStatus.CREATED
        assert response["multiValueHeaders"]["Location"]

    def test_get_farmer_by_id(self) -> None:
        # Create a farmer to have data to retrieve
        create_request = {
            "email": "jacques.martin@fermier.fr",
            "firstName": "Jacques",
            "lastName": "Martin",
            "phoneNumber": "+33 987654321",
        }

        create_response = lambda_handler(
            *create_api_call(FARMER_BASE_PATH, HTTPMethod.POST, body=create_request)
        )
        assert create_response["statusCode"] == HTTPStatus.CREATED
        location = create_response["multiValueHeaders"]["Location"][0]

        # Get the farmer by ID
        get_response = lambda_handler(
            *create_api_call(
                location,
                HTTPMethod.GET,
            )
        )

        # Assert the response
        assert get_response["statusCode"] == HTTPStatus.OK

        assert json.loads(get_response["body"]) == {
            "reference": location.removeprefix(f"{FARMER_BASE_PATH}/"),
            "firstName": "Jacques",
            "lastName": "Martin",
            "email": "jacques.martin@fermier.fr",
            "phoneNumber": "+33987654321",
        }
