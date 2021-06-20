from databases.core import Database
import functools
import asyncio
import pytest

from duck_orm.Model import Model
from duck_orm.sql import fields as Field
from duck_orm.sql.relationship import ManyToOne, OneToOne, OneToMany

db = Database('postgresql://postgres:arquinator2020@localhost:5432/orm')


class City(Model):
    __tablename__ = 'cities'
    __db__ = db

    id: int = Field.Integer(
        primary_key=True, auto_increment=True)
    name: str = Field.String(unique=True)

    @classmethod
    def relationships(cls):
        cls.persons = OneToMany(
            model=Person, name_in_table_fk='city', name_relation='person_city')


class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id: int = Field.Integer(
        primary_key=True, auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)
    salary: int = Field.BigInteger()
    city: City = ManyToOne(model=City)


class Contact(Model):
    __tablename__ = 'contacts'
    __db__ = db

    id_person: Person = OneToOne(model=Person)
    phone: str = Field.String(not_null=True)


# Creating instances of Cities.
city_cg = City(name="Campina Grande")
city_kh = City(name="Konoha")

# Creating instances of Persons.
person_1 = Person(first_name="Rich", last_name="Ramalho",
                  age=22, salary=1250, city=city_cg)
person_2 = Person(first_name="Elton", last_name="Ramalho",
                  age=22, salary=1250)
person_3 = Person(first_name="Naruto", last_name="Uzumaki",
                  age=16, salary=500000)
person_4 = Person(first_name="Hinata", last_name="Hyuga",
                  age=16, salary=500000)

# Creating instances of Contacts.
# contact_person_1 = Contact(phone="XXXXXXXXX-XXXX", id_person=person_1)
# contact_person_2 = Contact(phone="YYYYYYYYY-YYYY", id_person=person_2)
# contact_error = Contact(phone="YYYYYYYYY-YYYY", id_person=person_2)


def async_decorator(func):
    """
    Decorator used to run async test cases.
    """

    @functools.wraps(func)
    def run_sync(*args, **kwargs):
        loop = asyncio.get_event_loop()
        task = func(*args, **kwargs)
        return loop.run_until_complete(task)

    return run_sync


def test_model_class():
    assert City._get_name() == 'cities'
    assert Person._get_name() == 'persons'
    # assert Contact._get_name() == 'contacts'
    # assert isinstance(Contact.id_person, OneToOne)
    assert isinstance(Person.city, OneToMany)


def test_create_sql():
    sql = Person.__get_create_sql()
    assert sql == "CREATE TABLE IF NOT EXISTS persons (" + \
        "salary BIGINT, " + \
        "last_name TEXT NOT NULL, " + \
        "id SERIAL PRIMARY KEY, " + \
        "first_name TEXT UNIQUE, " + \
        "age BIGINT, " + \
        "city INTEGER, " + \
        " FOREIGN KEY (city) REFERENCES cities (id));"


def get_table(table, tables):
    for tup in tables:
        if (tup['tablename'] == table):
            return True
    return False


@async_decorator
async def test_create_table():
    await db.connect()
    await City.create()
    await Person.create()
    await Contact.create()
    tables = await Person.find_all_tables()
    assert get_table('persons', tables)
    assert get_table('contacts', tables)
    assert get_table('cities', tables)


@async_decorator
async def test_save_city():
    global city_cg
    global city_kh
    city_cg = await City.save(city_cg)
    city_kh = await City.save(city_kh)
    assert city_kh.name == 'Konoha'
    assert city_cg.name == 'Campina Grande'


@async_decorator
async def test_save_person():
    global person_1
    global person_2
    global person_3
    person_1 = await Person.save(person_1)
    person_2 = await Person.save(person_2)
    person_3 = await Person.save(person_3)
    assert person_1.first_name == 'Rich'
    assert person_2.first_name == 'Elton'
    assert person_3.first_name == 'Naruto'


@async_decorator
async def test_save_contact():
    global contact_person_1
    global contact_person_2
    global contact_error
    contact_person_1 = await Contact.save(contact_person_1)
    contact_person_2 = await Contact.save(contact_person_2)
    assert contact_person_1.phone == 'XXXXXXXXX-XXXX'
    assert contact_person_2.phone == 'YYYYYYYYY-YYYY'

    with pytest.raises(Exception):
        contact_error = await Contact.save(contact_error)


@async_decorator
async def test_drop_table():
    await Contact.drop_table()
    await Person.drop_table()
    await City.drop_table()
