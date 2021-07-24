# Methods

Here we will show some methods that the Model has and we will also see how to
use each one of them.

**To run the examples run using `ipython`.**

## get_name

Method that returns the name of the `Model` in the database.

And if the `__tablename__` attribute has not been assigned in the `Model`, then
this method will return the class name in lowercase.

``` python hl_lines="7 16"
class Person(Model):
    __db__ = db

    id_teste: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)

Person.get_name() # will return 'person'.

class Client(Model):
    __tablename__ = 'clients'
    __db__ = db

    # definitions of fields
    ...

Client.get_name() # Will return 'clients'.
```

## create

Asynchronous method that will create the table that represents the `Model` 
in the database of data.

It should always be used **before** trying to save, search or delete an object
of the `Model`.

``` python hl_lines="11"
class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id_teste: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)
    salary: int = Field.BigInteger()

await Person.create()
```

## save

``` python
save(model: Model) -> Model:
```

Asynchronous method that will save an object to the table in the database.

- Parameters:
    - `model`: `Model` instance with fields filled.

``` python
...

person_1 = Person(
    first_name="Teste 1", last_name="teste lastname", age=19, salary=5000)
person_2 = Person(
    first_name="Teste 2", last_name="teste lastname", age=25, salary=4000)
person_3 = Person(
    first_name="Teste 3", last_name="teste lastname", age=22, salary=2500)

person_1 = await Person.save(person_1)
person_2 = await Person.save(person_2)
person_3 = await Person.save(person_3)

person_1.id # 1
person_1.first_name # Teste 1
person_1.age # 19

person_2.id # 2
person_2.first_name # Teste 2
person_2.age # 25

person_3.id # 3
person_3.first_name # Teste 3
person_3.age # 22

```

## find_all

``` python
find_all(
    fields_includes: List[str] = [],
    fields_excludes: List[str] = [],
    conditions: List[Condition] = [],
    limit: int = None
) -> List[Model]
```

Asynchronous method that retrieves all objects persisted in a table in the
database.

- Parameters:
    - `fields_includes`: The `Model` fields that are to be retrieved.
    - `fields_excludes`: The `Model` fields that should not be retrieved.
    - `conditions`: Conditions for filtering objects.
    - `limit`: The maximum limit of objects that must be retrieved.

``` python
...

from duck_orm.sql.condition import Condition

persons: list[Person] = await Person.find_all(
    fields_includes=['first_name', 'age', 'salary'],
    # I could have left this parameter blank as it is no longer in 
    # fields_includes.
    fields_excludes=['id'],
    conditions=[
        Condition('first_name', 'LIKE', 'Teste%'),
        Condition('salary', '>=', 2600)
    ]
)

for person in persons:
    print(person.id_teste)  # None em todos.
    print(person.first_name)  # Teste 1, Teste 2
    print(person.age)  # 19, 25
    print(person.salary)  # 5000, 4000
```

### find_one

``` python
find_all(
    fields_includes: List[str] = [],
    fields_excludes: List[str] = [],
    conditions: List[Condition] = [],
) -> List[Model]
```

Asynchronous method that retrieves only one object persisted in a table in the
database. If you pass the filtering condition by the key field, this
method can be used as a find by id.

- Parameters:
    - `fields_includes`: The `Model` fields that are to be retrieved.
    - `fields_excludes`: The `Model` fields that should not be retrieved.
    - `conditions`: The conditions for filtering the object.

``` python
person: Person = await Person.find_one(
    conditions=[
        Condition('id_teste', '=', 1)
    ]
)

print(person.id_teste)  # 1
print(person.first_name)  # Teste 1
print(person.last_name)  # teste lastname
print(person.age)  # 19
print(person.salary)  # 5000
```

### find_all_tables

``` python
async def find_all_tables():
```

Asynchronous method that returns all table names persisted in the database
of data.

``` python
print(await Person.find_all_tables())
```

### update

``` python
async def update(self, **kwargs) -> Model:
```

Asynchronous method to alter a record persisted in the database.

- Parameters:
    - `kwargs`: A dictionary with the `Model` fields that must be changed
    and its new values.

``` python
person: Person = await Person.find_one(
    conditions=[
        Condition('id_teste', '=', 1)
    ]
)

print(person.id_teste)  # 1

person: Person = await person.update(first_name='Teste 1 UPDATE', age=22)

print(person.id_teste) # 1
print(person.first_name) # Teste 1 UPDATE
print(person.age) # 22
```

### delete

``` python
async def delete(cls, conditions: List[Condition]):
```

Asynchronous method that deletes a record from the database.

- Parameters:
    - `conditions`: The conditions for filtering the record(s).

``` python
person: Person = await Person.delete(
    conditions=[
        Condition('id_teste', '=', 1)
    ]
)
```
