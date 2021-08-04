# Duck ORM

The `Duck-ORM` package is an asynchronous ORM for Python, with support for **Postgres** and **SQLite**. ORM is built with:

- [databases](https://github.com/encode/databases)

**Requirements**: Python 3.8+

**Duck-ORM is still under development**.

## Installation

```bash
$ pip install duck-orm
```

## Quickstart

For this example we will create a connection to the SQLite database and create a model.

```bash
$ pip install databases[sqlite]
$ pip install ipython
```

Note that we want to use `ipython` here, because it supports using await expressions directly from the console.

### Creating the connection to the SQLite database:

```Python
from databases import Database
from duck_orm.Model import Model

db = Database('sqlite:///example.db')
await db.connect()
```

### Defining a model:

```Python
from duck_orm.sql import fields as Field

class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)

# Table creation in the database.
await Person.create()
```

- The `__tablename__` attribute is used to define the table's name in the database.
- The `__db__` attribute is the instance of the database connection.
- And then the definition of the fields, their types and restrictions.
- And finally, the table creation in the database.

## License

`DuckORM` is built as an open-source tool and remains completely free(MIT license).
