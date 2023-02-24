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

    name: str = Field(
        ...,
        max_length=30,
        title="Nombre",
        description="El nombre completo de la persona",
        example='Luisana Perez'
    )

    age: int = Field(
        ...,
        title="Edad",
        description="La edad de la persona",
        example=15
    )

    phone: str  = Field(
        ...,
        title="Numero de telefono",
        description="Numero de telefono de la persona",
        example="042412568"
    )
