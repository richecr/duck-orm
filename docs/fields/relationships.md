# Relationships

The relationships supported by `DuckORM` are basically of two types:

- One to Many and Many to One are supported by the `ForeignKey` field.
- Many to Many by creating a table and making use of the `ForeignKey` field to
relate the two tables.
- One to One with the `OneToOne` field.

Let's look at some examples of using these fields.

## ForeignKey

- Set the `ForeignKey` field to use a One-to-Many relationship.

``` python hl_lines="25"
class City(Model):
    __tablename__ = 'cities'
    __db__ = db

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    name: str = Field.String(unique=True)

    def relationships(self):
        self.persons = OneToMany(
            model=Person,
            name_in_table_fk='city',
            name_relation='person_city'
        )


class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id_teste: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger()
    salary: int = Field.BigInteger()
    city: City = ForeignKey(model=City, name_in_table_fk='id')

await City.create()
await Person.create()
```

And with that, it will create the two tables and the `persons` table will have 
a field referencing the `id` field of the `cities` table.

!!! note
    You may have also noticed the `relationships` method in the `City` class. But
    what will this be?

    This method doesn't do anything else, it doesn't make any changes to the database, just
    adds the `persons: OneToMany` field to the class, this field has some methods
    which are explained [here](./one_to_many.md). 


## ManyToMany

- To create a Many to Many relationship we also use the `ForeignKey` field.

``` python  hl_lines="32-33"
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
    working_days: WorkingDay = ForeignKey(model=WorkingDay, name_in_table_fk='id')

await User.create()
await WorkingDay.create()
await UsersWorkingDay.create()
```

First we create the `User` and 'WorkingDay` tables, they have a Many to Many
relationship. To represent this relationship we create a third `UsersWorkingDay`
table that has a reference to the `PK` of the other two tables, and thus 
creating the relationship.

!!! note
    The `relationships` method in the two tables: `User` and `WorkingDay` are a little bit
    different from the previous example. Have the `@classmethod` signaling that it is a
    method of the class and not the instance, so it creates the `users` and
    `working_day` in both models. 
    
    With that allowing some methods to be executed,
    like: `User` add a relationship with `WorkingDay` without using the
    `UsersWorkingDay` model. More examples can be seen [here](./many_to_many.md).

