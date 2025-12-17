from abc import ABC, abstractmethod

from maypy import Maybe

from mill_sime.domain.models.farmer import Farmer, FarmerReference


class FarmerRepository(ABC):
    @abstractmethod
    def get_by_reference(self, reference: FarmerReference) -> Maybe[Farmer]: ...

    @abstractmethod
    def save(self, farmer: Farmer) -> None: ...

    @abstractmethod
    def exists(self, email: str) -> bool: ...
