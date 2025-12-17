from collections.abc import Iterator

import pytest
from sqlalchemy.orm import Session
from tests.fixtures.db import get_sqlite_engine
from tests.fixtures.farmer_fixtures import create_farmer

from mill_sime.secondary.farmer_repository import SqlAlchemyFarmerRepository
from mill_sime.secondary.tables import FarmerModel


class TestSqlAlchemyFarmerRepository:
    @pytest.fixture(autouse=True)
    def setup(self) -> Iterator[None]:
        with get_sqlite_engine() as engine:
            self.engine = engine
            self.repository = SqlAlchemyFarmerRepository(engine)

            yield

    def test_save(self) -> None:
        # Given
        farmer = create_farmer()

        # When
        self.repository.save(farmer)

        # Then
        with Session(self.engine) as session:
            result = session.query(FarmerModel).all()

            assert result == [FarmerModel.from_domain(farmer)]

    def test_get_farmer_by_reference(self) -> None:
        # Given
        farmer = create_farmer()
        self.repository.save(farmer)

        # When
        result = self.repository.get_by_reference(farmer.reference)

        # Then
        assert result.is_present()
        assert result.get() == farmer

    def test_get_farmer_by_reference_should_return_empty_when_not_found(self) -> None:
        # When
        result = self.repository.get_by_reference(create_farmer().reference)

        # Then
        assert result.is_empty()

    def test_exists_should_return_true_when_farmer_exists(self) -> None:
        # Given
        farmer = create_farmer()
        self.repository.save(farmer)

        # When / Then
        assert self.repository.exists(farmer.email)

    def test_exists_should_return_false_when_farmer_not_found(self) -> None:
        assert not self.repository.exists("unit.test@tdd.com")
