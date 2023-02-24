from pydantic import (
    BaseModel,
    Field
)

class TransactionBase(BaseModel):
    username: str = Field(
        ...,
        max_length=30,
        title="Nombre de usuario",
        description="Es el nombre de usuario de quien ejecuta la transaccion",
        example='Luisana16'
    )

    amount: int = Field(
        ...,
        title="Monto",
        description="Monto de la transaccion",
        example=500
    )
    
class TransactionSegutity(TransactionBase):
    password: str = Field(
        ...,
        min_length=3,
        max_length=30,
        title="Contrasenha",
        description="La contrasenha de la cuenta",
        example="noUseThisPassword00"
    )    