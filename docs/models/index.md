# Models

With `DuckORM` it's easy to create your database models and get started right away.

``` python hl_lines="10"
from databases import Database

from duck_orm.model import Model
from duck_orm.sql import fields as Field

db = Database('sqlite:///example.db')
await db.connect()


class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)
    salary: int = Field.BigInteger()
```

So far you've only defined a template, but you haven't told DuckORM to create
a table in the database, but it's easy to do that, just add a line of code:

``` python
await Person.create()
```

## Definition of fields

And then just define the table [fields](../fields/index.md).

### Basic Types

For each table created, it must necessarily have a field with the attribute
`primary_key=True`.

And only one `primary_key` column is allowed.

``` python hl_lines="5-9"
class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)
    salary: int = Field.BigInteger()
```

!!! warning 
    You should not assign more than one `primary_key` to more than one column 
    in the same table.

## Dependencies

`DuckORM` depends on `databases` library to connect to the database.

### Databases

This parameter is `it `, and it is the instance create, bith your database 
URL string.

This instance needs to be passed to the `Model`.

``` python hl_lines="1 6 7 12"
from databases import Database

from duck_orm.model import Model
from duck_orm.sql import fields as Field

db = Database('sqlite:///example.db')
await db.connect()


class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)
    salary: int = Field.BigInteger()
```

!!! tip
    You must create the `databases` instance **only once** and then
    use it for all models of your system, but nothing stops you from creating
    **multiple instances**Another important parameter is __tablename__, which is used to set the name of your Model in the database. if you want to use **multiple databases**.

### Table names

Another important parameter is `__tablename__`, which is used to set the name
 of your Model in the database.

``` python hl_lines="2"
class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)
    salary: int = Field.BigInteger()
```

!!! tip
    If you don't pass the `__tablename__` attribute, the table name will be
    defined by the name of the `Model`.
    
    **Example:** In the case above, if the `__tablename__` attribute was not passed, the name
    of the table would be `person`.
