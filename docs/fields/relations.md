# Relationships

The relationships supported by `DuckORM` are basically of two types:

- One to Many and Many to One are supported by the `ForeignKey` field.
- Many to Many by creating a table and making use of the `ForeignKey` field to
relate the two tables.
- One to One with the `OneToOne` field.

Let's look at some examples of using these fields.

## OneToMany

- Set the [ForeignKey](./foreignkey.md) field to use a One-to-Many relationship.

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
    You may have also noticed the method `relationships` in the `City` class, 
    but what will this do?

    This method doesn't make any changes to the database, just
    adds the `persons: OneToMany` field to the class, this field has some methods
    which are explained [here](./one_to_many.md). 


## ManyToMany

- To create a [Many to Many](./many_to_many.md) relationship we also use the `ForeignKey` field.

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

First we create the `User` and `WorkingDay` tables, they have a Many to Many
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

## OneToOne

- To represent the [One to One](./one_to_one.md) relationship, just make use of the `OneToOne` field.

``` python  hl_lines="16-20"
class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id_teste: int = Field.Integer(primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger()
    salary: int = Field.BigInteger()


class Contact(Model):
    __tablename__ = 'contacts'
    __db__ = db

    id_person: Person = OneToOne(
        model=Person,
        name_relation='person_contact',
        field='id_person'
    )
    phone: str = Field.String(not_null=True)

await Person.create()
await Contact.create()
```

We create the `Person` table and the `Contact` table. We use the `OneToOne` field.
This field will be the `PK` of that table, being of the same type as the table in the
relationship, in this case the same type as the `PK` of the `Person` model.

To save a Contact record:

``` python hl_lines="2 5"
person_1 = Person(first_name="Rich", last_name="Ramalho", age=22, salary=1250)
contact_person_1 = Contact(phone="XXXXXXXXX-XXXX", id_person=person_1)

person_1 = await Person.save(person_1)
contact_person_1 = await Contact.save(contact_person_1)
```

And with that, `DuckORM` will save the relationship contact record
with this person. What happens if I try to save the same person again in a
another contact?

``` python hl_lines="3 4"
contact_error = Contact(phone="YYYYYYYYY-YYYY", id_person=person_1)

await Contact.save(contact_error) # This line will throw a duplicate 
                                  # record exception.
```