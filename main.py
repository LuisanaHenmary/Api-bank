from fastapi import (
    FastAPI,
    status,
    HTTPException,
    Body,
    Path
)

from models.person import Person
from models.account import (
    Account,
    AccountRegister
)

from models.transaction import (
    TransactionBase,
    TransactionSegutity
)

from database.models import (
    People as p,
    AccountsBank as c
)

from helpers.bank_actions import (
    login,
    insert_transaction,
    update_balance
)

app = FastAPI()

@app.get("/")
def read_root():

    return {"Hello": "World"}

@app.post(
    path="/add/people",
    tags=["Add"],
    status_code=status.HTTP_201_CREATED,
    summary="Registers a new user"
)
def register_people(people: Person=Body(...)):

    try:
        p.insert(
            ci=people.ci,
            name=people.name,
            age=people.age,
            phone_number=people.phone
        ).execute()
    except Exception as error:
        number_error, message_error = error.args
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"error {number_error}: {message_error}"
        )
    
    return people

@app.post(
    path="/add/account",
    tags=["Add"],
    response_model=Account,
    status_code=status.HTTP_201_CREATED,
    summary="Registers a new account"
)
def add_account(account: AccountRegister=Body(...)):

    try:
        c.insert(
            ci_id = account.ci,
            username = account.username,
            type_account = account.type_account,
            balance = account.balance,
            password = account.password
        ).execute()
    except Exception as error:
        number_error, message_error = error.args
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"error {number_error}: {message_error}"
        )

    return account
    

@app.put(
    path="/to/deposit",
    tags=["Bank actions"],
    response_model=TransactionBase
)
def to_deposit(
    transaction: TransactionSegutity=Body(...)
):
    amount = transaction.amount
    try:
        ci, num_account, old_balance = login(transaction.username, transaction.password)
        
        new_balance = old_balance + amount

        update_balance(num_account,new_balance)
        
        insert_transaction(ci,num_account,"Deposit", amount)
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    return transaction

@app.put(
    path="/to/withdrawal",
    tags=["Bank actions"],
    response_model=TransactionBase
)
def to_withdrawal(transaction: TransactionSegutity=Body(...)):

    amount = transaction.amount
    try:
        ci, num_account, old_balance = login(transaction.username, transaction.password)
        
        new_balance = old_balance - amount

        update_balance(num_account,new_balance)
        
        insert_transaction(ci,num_account,"Withdrawal",(amount*(-1)))
        
    except Exception:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid username or password"
        )

    return transaction

@app.put(
    path="/to/transfer/{receiver}",
    tags=["Bank actions"],
    response_model=TransactionBase
)
def to_transfer(receiver: str = Path(
    ..., title="Nombre del usuario del receptor",
    description="El nombre del usuario del receptor"
    ),
    transaction: TransactionSegutity=Body(...)
    ):

    amount = transaction.amount
    try:
        ci, num_account, old_amount = login(transaction.username, transaction.password)

        query = (c.
        select()
        .where(c.username == receiver)
        )

        reciver_ci = query[0].ci_id
        reciver_num = query[0].num_account

        transmitter_balance = old_amount - amount
        receiver_balance = query[0].balance + amount

        update_balance(num_account,transmitter_balance)
        update_balance(reciver_num,receiver_balance)

        insert_transaction(ci,num_account,"Transfer",(amount*(-1)))
        insert_transaction(reciver_ci,reciver_num,"Transfer",amount)

    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )

    return transaction

@app.get(
    path="/balance/{enum}",
    tags=["Bank actions"],
)
def inquiry_balance(num_account: int = Path(
    ..., title="Numero de la cuenta",
    description="El numero de la cuenta en la que se quiere consultar el saldo"
    )):

    current_balance = 0

    try:
        querry = (
            c.select()
            .where(c.num_account == num_account)
            )

        current_balance = querry[0].balance
        ci_own = querry[0].ci_id

    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Account dont exist"
        )

    return {"Account number":num_account,"CI person": ci_own,"Balance":current_balance}
    
