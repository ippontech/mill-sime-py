from mill_sime.domain.models.farmer import FarmerReference


class BusinessError(Exception):
    """Global business error."""


class AlreadyExistsError(BusinessError):
    """Global already exists error."""


class NotFoundError(BusinessError):
    """Global not found error."""


class FarmerAlreadyExistsError(AlreadyExistsError):
    def __init__(self, email: str) -> None:
        super().__init__(f"Farmer with email {email} already exists.")


class FarmerNotFoundError(NotFoundError):
    def __init__(self, reference: FarmerReference) -> None:
        super().__init__(f"Farmer with reference {reference} not found.")
