#pydantic
from pydantic import (
    BaseModel,
    Field
)

class Person(BaseModel):

    ci: str  = Field(
        ...,
        title="Cerdula",
        description="Cerdula de la persona",
        example='V-26852997'
    )

    first_name: str = Field(
        ...,
        max_length=30,
        title="Nombre",
        description="El primer nombre de la persona",
        example='Luisana'
    )

    last_name: str = Field(
        ...,
        max_length=30,
        title="Apellido",
        description="El apellido de la persona",
        example='Perez'
    )
