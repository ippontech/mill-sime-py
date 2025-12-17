from collections.abc import Iterator
from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient
from pydantic_extra_types.phone_numbers import PhoneNumber
from tests.fixtures.db import get_sqlite_engine

from mill_sime.dependencies import get_engine
from mill_sime.primary.main import app
from mill_sime.primary.routes.farmer import FARMER_BASE_PATH


class TestFarmerResource:
    @pytest.fixture(autouse=True)
    def setup(self) -> Iterator[None]:
        with TestClient(app) as client, get_sqlite_engine() as engine:
            self.client = client
            self.engine = engine
            app.dependency_overrides[get_engine] = lambda: engine

            yield

            app.dependency_overrides = {}

    def test_create_new_farm(self) -> None:
        request = {
            "email": "jean.dupont@fermier.fr",
            "firstName": "Jean",
            "lastName": "Dupont",
            "phoneNumber": "+33 123456789",
        }
        response = self.client.post(FARMER_BASE_PATH, json=request)

        assert response.status_code == HTTPStatus.CREATED
        assert response.headers["Location"]

    def test_get_farmer_by_id(self) -> None:
        # Create a farmer to have data to retrieve
        create_request = {
            "email": "jacques.martin@fermier.fr",
            "firstName": "Jacques",
            "lastName": "Martin",
            "phoneNumber": "+33 987654321",
        }
        PhoneNumber()
        create_response = self.client.post(FARMER_BASE_PATH, json=create_request)
        assert create_response.status_code == HTTPStatus.CREATED
        location = create_response.headers["Location"]

        # Get the farmer by ID
        get_response = self.client.get(location)

        # Assert the response
        assert get_response.status_code == HTTPStatus.OK
        body = get_response.json()

        assert body == {
            "reference": location.removeprefix(f"{FARMER_BASE_PATH}/"),
            "firstName": "Jacques",
            "lastName": "Martin",
            "email": "jacques.martin@fermier.fr",
            "phoneNumber": "+33987654321",
        }
