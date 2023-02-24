from database.models import (
    AccountsBank,
    Transactions
)

#Estas son funciones mas usadas en los enpoints

import datetime

def login(username, password):
    query = (AccountsBank.
    select()
    .where((AccountsBank.username == username) & (AccountsBank.password == password))
    )

    ci = query[0].ci_id
    num_account = query[0].num_account
    old_balance = query[0].balance

    return (ci, num_account, old_balance)

def insert_transaction(ci, num_account, transaction_type, amount):
    Transactions.insert(
    ci_id = ci,
    num_account_id = num_account,
    type_tranction = transaction_type,
    amount = amount
    ).execute()

def update_balance(num_account, new_balance):
    AccountsBank.update(
    balance = new_balance,
    updated_at = datetime.datetime.now()
    ).where(AccountsBank.num_account == num_account).execute()