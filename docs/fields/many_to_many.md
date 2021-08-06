# ManyToMany

This field should represent the Many to Many relationship.
Let's look at some methods allowed by this field.

- The interface of a field `ManyToMany`:

``` python
ManyToMany(model: Model, model_relation: Model):
```

- Parameters:
    - `model`: The other `Model` that will be used in the relationship.
    - `model_relation`: The `Model` that represents the relationship table
    between the two models.

## Methods

Methods that are supported by the ManyToMany field.

### add_models

Takes instance of the two relationship models and then saves it to the
relationship table.

```python
async def add_models(
    model_instance_one: Model, model_instance_two: Model) -> Model:
```

- Parameters:
    - `model_instance_one`: An instance of the `Model` of the relation.
    - `model_instance_two`: An instance of the main `Model` that calls 
    the method.

### add

Method called from an instance of one model and you must pass the instance 
of the other model. The relationship between the two will be saved.

```python
async def add(model_instance_one: Model) -> Model:
```

- Parameters:
    - `model_instance_one`: An instance of the `Model` of the relation.

### get_all

Returns records from the other model of the relationship.

```python
async def get_all() -> list[Model]:
```

## Examples

First, let's create our templates.

Examples of using the methods explained above.

``` python
class User(Model):
    __tablename__ = 'users'
    __db__ = db

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    name: str = Field.String()

    @classmethod
    def relationships(cls):
        cls.working_day = ManyToMany(model=WorkingDay,
                                     model_relation=UsersWorkingDay)


class WorkingDay(Model):
    __tablename__ = 'working_days'
    __db__ = db

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    week_day: str = Field.String()
    working_date: str = Field.String()

    @classmethod
    def relationships(cls):
        cls.users = ManyToMany(model=User, model_relation=UsersWorkingDay)


class UsersWorkingDay(Model):
    __tablename__ = 'users_working_days'
    __db__ = db

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    users: User = ForeignKey(model=User, name_in_table_fk='id')
    working_days: WorkingDay = ForeignKey(
        model=WorkingDay, name_in_table_fk='id')

await User.create()
await WorkingDay.create()
await UsersWorkingDay.create()
```

- Can I use the `Add` and/or `add_models` method of the `ManyToMany` field to 
save a relationship:

``` python hl_lines="10 11 13 14"
user = await User.save(User(name='Rich'))
user1 = await User.save(User(name='Elton'))

working_day = WorkingDay(week_day='segunda', working_date='02/08/2021')
working_day1 = WorkingDay(week_day='terça', working_date='03/08/2021')

working_day = await WorkingDay.save(working_day)
working_day1 = await WorkingDay.save(working_day1)

await User.working_day.add_models(working_day, user)
await WorkingDay.users.add_models(user, working_day1)

await user1.working_day.add(working_day)
await user1.working_day.add(working_day1)

```

In lines 10, 11, 13 and 14 we are creating a record in the table
`UsersWorkingDay` which is responsible for the `Many to Many` relationship.

Do you notice a difference between lines 10-11 and 13-14?

In the first ones it uses the attribute that is not only on the instance, it calls the
from the models themselves, `User` and `WorkingDay`.

In the last two it uses the instance attribute of a `User`, so it uses
this instance to save in the relationship with the record that is passed as
parameter.


- We also have the `get_all` method:

``` python
users: list[User] = await working_day.users.get_all()

for u in users:
    print(u.id) # 1 and 2
    print(u.name) # 'Rich' and 'Elton'
```
