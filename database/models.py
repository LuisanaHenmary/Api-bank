import datetime

#Si se ejecuta directamente con python crear las tablas de la base de dato
#para hacer consultas usando ORM

from peewee import (
    MySQLDatabase,
    Model,
    DateTimeField,
    CharField,
    IntegerField,
    ForeignKeyField,
    AutoField
)

mysql_db = MySQLDatabase(
    'bank', #Nombre de la dase de datos
    user='root',
    password='', #Si es otra cambie el valor
    host='localhost',
    port=3306
)

class BaseModel(Model):
    created_at = DateTimeField(default = datetime.datetime.now )
    updated_at = DateTimeField(default = datetime.datetime.now )
    class Meta:
        database = mysql_db


class People(BaseModel):
    ci = CharField(primary_key=True, max_length=20)
    name = CharField(max_length=30)
    age = IntegerField()
    phone_number = CharField(max_length=20)

class AccountsBank(BaseModel):
    num_account = AutoField()
    ci = ForeignKeyField(People)
    username = CharField(max_length=30, unique=True)
    type_account  = CharField(max_length=10, default='Current')
    balance = IntegerField(default=0)
    password = CharField(max_length=20)


class Transactions(BaseModel):
    id = AutoField()
    ci = ForeignKeyField(People)
    num_account = ForeignKeyField(AccountsBank)
    amount = IntegerField(default=0)
    type_tranction  = CharField(max_length=10, default='current')


if __name__=="__main__":
    mysql_db.create_tables([People,AccountsBank, Transactions])