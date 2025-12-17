from pydantic import AliasGenerator, BaseModel, ConfigDict, EmailStr
from pydantic.alias_generators import to_camel


class FarmerOutput(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        alias_generator=AliasGenerator(serialization_alias=to_camel),
        json_schema_extra={
            "examples": [
                {
                    "reference": "e8cab89b-2751-4271-b1e4-9c3841be5d86",
                    "firstName": "Jean",
                    "lastName": "Dupont",
                    "email": "jean.dupont@fermier.fr",
                    "phoneNumber": "+33 123456789",
                }
            ]
        },
    )
    reference: str
    first_name: str
    last_name: str
    email: EmailStr
    phone_number: str
