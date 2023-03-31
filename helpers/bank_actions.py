from pymongo import MongoClient
from .exceptions import (
    InsufficientBalance
)

#Estas son funciones mas usadas en los enpoints

client = MongoClient('localhost', 27017)
db = client["bank"]
people_collection = db["people"]
account_collection = db["accounts"]
transaction_collection = db["transactions"]

def update_balance(transaction):
    account_select = account_collection.find_one({"number_account":transaction["number_account"]})
    old_balance = account_select["balance"]
    new_balance = old_balance + transaction["amount"]

    if new_balance < 0:
            raise InsufficientBalance()

    account_collection.find_one_and_update({
        "number_account":transaction["number_account"]},{"$set":{"balance":new_balance}})