from pydantic import (
    BaseModel,
    Field
)

from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    number_account: int = Field(
        ...,
        title="numero de cuenta",
        description="Es el numero de cuenta anfintriona",
        example=1
    )

    transactional_code: Optional[str] = Field(
        title="condigo transaccional",
        description="es el codigo de la transaccion",
    )

    amount: int = Field(
        ...,
        title="Monto",
        description="Monto de la transaccion",
        example=500
    )

    transaction_date: Optional[datetime] = Field(
        default=None,
        title="fecha",
        description="Es la fecha en que fue realizada la transaccion"
    )

class Transference(Transaction):
    number_account_receiver: int = Field(
        ...,
        title="numero de cuenta",
        description="Es el numero de cuenta del receptor",
        example=1
    )