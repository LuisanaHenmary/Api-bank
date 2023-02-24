from pydantic import (
    BaseModel,
    Field
)

class Account(BaseModel):

    ci: str  = Field(
        ...,
        title="Cedula",
        description="Cedula del propietario",
        example='V-26852997'
    )

    username: str = Field(
        ...,
        max_length=30,
        title="Nombre de usuario",
        description="Es el nombre de usuario",
        example='Luisana16'
    )

    type_account: str  = Field(
        ...,
        title="Tipo de cuenta",
        description="Es el tipo de cuenta bancaria",
        example="Ahorro"
    )

    balance: int = Field(
        ...,
        title="Saldo",
        description="El saldo disponible",
        example=0
    )


class AccountRegister(Account):
    password: str = Field(
        ...,
        min_length=8,
        max_length=64,
        title="Contrasenha",
        description="La contrasenha de la cuenta",
        example="noUseThisPassword00"
    )