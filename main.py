import threading

from fastapi import (
    FastAPI,
    status,
    HTTPException,
    Body,
    Path
)

from datetime import datetime
from uuid import uuid4

from models.person import Person

from models.account import Account

from models.transaction import (
    Transaction,
    Transference
)

from helpers.exceptions import (
    CIExist,
    CIDontExist,
    AccountDontExist,
    InsufficientBalance
)

from helpers.bank_actions import (
    people_collection,
    account_collection,
    transaction_collection,
    update_balance
)

app = FastAPI()

lock = threading.Lock()

@app.get("/")
def read_root():

    return {"Hello": "World"}

@app.post(
    path="/add/people",
    tags=["Add"],
    status_code=status.HTTP_201_CREATED,
    summary="Registers a new user"
)
def register_person(person: Person=Body(...)):

    try:
        if people_collection.count_documents({'ci':person.ci}) > 0:
            raise CIExist(person.ci)
        
        people_collection.insert_one(dict(person))
        
    except CIExist as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(error)
        )
    
    return person

@app.post(
    path="/add/account",
    tags=["Add"],
    status_code=status.HTTP_201_CREATED,
    summary="Registers a new account"
)
def add_account(account: Account=Body(...)):

    try:

        if people_collection.count_documents({"ci":account.ci}) == 0:
            raise CIDontExist(account.ci)

        account.number_account = account_collection.count_documents({})
        account.created_at = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        account_collection.insert_one(dict(account))

    except CIDontExist as error:
        
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail=str(error)
        )

    return account

@app.put(
    path="/to/deposit",
    tags=["Bank actions"]
)
def to_deposit(
    transaction: Transaction=Body(...)
):
    
    try:
        if account_collection.count_documents({"number_account":transaction.number_account}) == 0:
            raise AccountDontExist(transaction.number_account)

        update_balance(dict(transaction))

        transaction.transaction_date = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

        while True:
            aux = str(uuid4())

            if transaction_collection.count_documents({"transactional_code":aux}) == 0:
                transaction.transactional_code = aux
                break

        
        transaction_collection.insert_one(dict(transaction))
            
    except AccountDontExist as error:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=str(error)
        )

    return transaction

@app.put(
    path="/to/withdrawal",
    tags=["Bank actions"]
)
def to_withdrawal(transaction: Transaction=Body(...)):

    try:
        if account_collection.count_documents({"number_account":transaction.number_account}) == 0:
            raise AccountDontExist(transaction.number_account)

        transaction.amount = transaction.amount*(-1)
        update_balance(dict(transaction))

        transaction.transaction_date = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

        while True:
            aux = str(uuid4())

            if transaction_collection.count_documents({"transactional_code":aux}) == 0:
                transaction.transactional_code = aux
                break

        transaction_collection.insert_one(dict(transaction))
        
    except AccountDontExist as error:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=str(error)
        )
    except InsufficientBalance as error:
        raise HTTPException(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        detail=str(error)
        )

    return transaction

@app.put(
    path="/to/transfer",
    tags=["Bank actions"]
)
def to_transfer(transaction: Transference=Body(...)):
    try:
        if account_collection.count_documents({"number_account":transaction.number_account}) == 0:
            raise AccountDontExist(transaction.number_account)

        if account_collection.count_documents({"number_account":transaction.number_account_receiver}) == 0:
            raise AccountDontExist(transaction.number_account_receiver)

        update_balance({
            "number_account":transaction.number_account,
            "amount":transaction.amount*(-1)
        })

        update_balance({
            "number_account":transaction.number_account_receiver,
            "amount":transaction.amount
        })

        transaction.transaction_date = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

        while True:
            aux = str(uuid4())

            if transaction_collection.count_documents({"transactional_code":aux}) == 0:
                transaction.transactional_code = aux
                break
        
        transaction_collection.insert_one(dict(transaction))

        return transaction

    except AccountDontExist as error:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=str(error)
        )
    except InsufficientBalance as error:
        raise HTTPException(
        status_code=status.HTTP_402_PAYMENT_REQUIRED,
        detail=str(error)
        )

@app.get(
    path="/balance/{number_account}",
    tags=["Bank actions"],
)
def inquiry_balance(number_account: int = Path(
    ..., title="Numero de la cuenta",
    description="El numero de la cuenta en la que se quiere consultar el saldo"
    )):


    account_select = account_collection.find_one({"number_account":number_account})
    balance = account_select["balance"]
    ci = account_select["ci"]
    return {
        "ci":ci,
        "number_account":number_account,
        "balance":balance
    }
    
