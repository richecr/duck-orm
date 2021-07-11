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

    id_teste: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)
    salary: int = Field.BigInteger()
```

So far you've only defined a template, but you haven't told DuckORM to create
a table in the database, but it's easy to do that, just add a line of code:

``` python
...
await Person.create()
```

## Definition of fields

And then just define the table [fields](../fields.md).

### Basic Types

For each table created, it must necessarily have a field with the attribute
`primary_key=True`.

And only one `primary_key` column is allowed.

``` python hl_lines="5-9"
class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id_teste: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)
    salary: int = Field.BigInteger()
```

!!! warning 
    You should not assign more than one `primary_key` to more than one column in the same table.