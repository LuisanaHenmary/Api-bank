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
from typing import List
from models.person import Person

from models.account import Account

from models.transaction import Transaction

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

        transaction.transaction_date = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

        while True:
            aux = str(uuid4())

            if transaction_collection.count_documents({"transactional_code":aux}) == 0:
                transaction.transactional_code = aux
                break

        data = dict(transaction)

        data.pop('number_account_receiver')

        update_balance(data)
        transaction_collection.insert_one(data)
            
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

        transaction.transaction_date = datetime.today().strftime("%d-%m-%Y %H:%M:%S")

        while True:
            aux = str(uuid4())

            if transaction_collection.count_documents({"transactional_code":aux}) == 0:
                transaction.transactional_code = aux
                break
        
        data = dict(transaction)

        data.pop('number_account_receiver')

        update_balance(data)

        transaction_collection.insert_one(data)
        
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
def to_transfer(transaction: Transaction=Body(...)):

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
        
        transfer = dict(transaction)

        transfer["amount"] = transaction.amount*(-1)
        transfer["receiver_amount"] = transaction.amount

        transaction_collection.insert_one(transfer)

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
    response_model=Account,
    tags=["Bank actions"],
)
def inquiry_balance(number_account: int = Path(
    ..., title="Numero de la cuenta",
    description="El numero de la cuenta en la que se quiere consultar el saldo"
    )):


    account_select = dict(account_collection.find_one({"number_account":number_account}))
    account_select.pop("_id")
    account_select["created_at"] = datetime.strptime(account_select["created_at"],"%d-%m-%Y %H:%M:%S")

    return account_select


@app.get(
    path="/accounts/{ci}",
    response_model=List[Account]
)
def get_accounts(ci: str = Path(
    ..., title="Cedula",
    description="Es la cedula de la persona")):


    accounts = list(account_collection.find({"ci":ci}))

    for i in range(len(accounts)):
        accounts[i].pop('_id')
        accounts[i]["created_at"] = datetime.strptime(accounts[i]["created_at"],"%d-%m-%Y %H:%M:%S")
        
    return accounts

    

@app.get(
    path="/transactions/{number_account}",
    response_model=List[Transaction]
)
def get_transactions(number_account: int = Path(
    ..., title="Numero de la cuenta",
    description="El numero de la cuenta en la que se quiere consultar el saldo"
    )):

    transactions = list(transaction_collection.find({"number_account":number_account}))

    for i in range(len(transactions)):
        transactions[i].pop('_id')
        transactions[i]["transaction_date"] = datetime.strptime(transactions[i]["transaction_date"],"%d-%m-%Y %H:%M:%S")

    return transactions