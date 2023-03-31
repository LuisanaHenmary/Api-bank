from pydantic import (
    BaseModel,
    Field,
    
)

from datetime import datetime
from typing import Optional

class Account(BaseModel):

    ci: str  = Field(
        ...,
        title="Cedula",
        description="Cedula del propietario",
        example='V-26852997'
    )

    number_account: Optional[int] = Field(
        title="numero de cuenta",
        description="Es el numero de cuenta",
    )

    balance: int = Field(
        ...,
        title="Saldo",
        description="El saldo disponible",
        example=0
    )

    created_at: Optional[datetime] = Field(
        default=None,
        title="fecha de apertura",
        description="Es la fecha en que fue creada"
    )