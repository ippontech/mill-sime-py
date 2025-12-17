from typing import Annotated

from pydantic import BaseModel, ConfigDict, EmailStr, Field
from pydantic.alias_generators import to_camel
from pydantic_extra_types.phone_numbers import PhoneNumber, PhoneNumberValidator

from mill_sime.domain.models.farmer import Farmer

type E164PhoneNumber = Annotated[PhoneNumber, PhoneNumberValidator(number_format="E164")]


class CreateFarmerRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        alias_generator=to_camel,
        json_schema_extra={
            "examples": [
                {
                    "firstName": "Jean",
                    "lastName": "Dupont",
                    "email": "jean.dupont@fermier.fr",
                    "phoneNumber": "+33 123456789",
                }
            ]
        },
    )

    first_name: Annotated[str, Field(min_length=1)]
    last_name: Annotated[str, Field(min_length=1)]
    email: EmailStr
    phone_number: E164PhoneNumber

    def to_domain(self) -> Farmer:
        return Farmer(
            first_name=self.first_name,
            last_name=self.last_name,
            email=str(self.email),
            phone_number=str(self.phone_number),
        )
