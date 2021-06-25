from databases.core import Database
import functools
import asyncio
import pytest

from duck_orm.model import Model
from duck_orm.sql import fields as Field
from duck_orm.sql.relationship import ManyToOne, OneToOne, OneToMany

db = Database('postgresql://postgres:arquinator2020@localhost:5432/orm')


class City(Model):
    __tablename__ = 'cities'
    __db__ = db

    id: int = Field.Integer(
        primary_key=True,
        auto_increment=True)
    name: str = Field.String(unique=True)

    @classmethod
    def relationships(cls):
        cls.persons = OneToMany(
            model=Person,
            name_in_table_fk='city',
            name_relation='person_city')


class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id_teste: int = Field.Integer(
        primary_key=True,
        auto_increment=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.BigInteger(min_value=18)
    salary: int = Field.BigInteger()
    city: City = ManyToOne(model=City)


class Contact(Model):
    __tablename__ = 'contacts'
    __db__ = db

    id_person = Field.Integer(primary_key=True)
    phone: str = Field.String(not_null=True)

    @classmethod
    def relationships(cls):
        cls.id_person: Person = OneToOne(
            model=Person,
            name_relation='person_contact',
            field='id_person')


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
    assert City.get_name() == 'cities'
    assert Person.get_name() == 'persons'
    assert Contact.get_name() == 'contacts'
    assert isinstance(Person.city, ManyToOne)


def test_create_sql():
    sql = Person._Model__get_create_sql()
    assert sql == "CREATE TABLE IF NOT EXISTS persons (" + \
        "salary BIGINT, " + \
        "last_name TEXT NOT NULL, " + \
        "id_teste SERIAL PRIMARY KEY, " + \
        "first_name TEXT UNIQUE, " + \
        "age BIGINT, " + \
        "city INTEGER);"


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

    await City.associations()
    await Person.associations()
    await Contact.associations()

    tables = await Person.find_all_tables()
    assert get_table('persons', tables)
    assert get_table('contacts', tables)
    assert get_table('cities', tables)


@async_decorator
async def test_save_city():
    global city_cg
    global city_kh
    # Creating instances of Cities.
    city_cg = City(name="Campina Grande")
    city_kh = City(name="Konoha")
    city_cg = await City.save(city_cg)
    city_kh = await City.save(city_kh)
    assert city_kh.name == 'Konoha'
    assert city_cg.name == 'Campina Grande'


@async_decorator
async def test_save_person():
    global person_1
    global person_2
    global person_3
    # Creating instances of Persons.
    person_1 = Person(first_name="Rich", last_name="Ramalho",
                      age=22, salary=1250)
    person_2 = Person(first_name="Elton", last_name="Ramalho",
                      age=22, salary=1250)
    person_3 = Person(first_name="Naruto", last_name="Uzumaki",
                      age=16, salary=500000)
    person_4 = Person(first_name="Hinata", last_name="Hyuga",
                      age=16, salary=500000)
    person_1_: Person = await city_kh.persons.add(person_1)
    person_2_: Person = await city_kh.persons.add(person_2)
    person_3_: Person = await city_kh.persons.add(person_3)
    assert person_1.id_teste == 1
    assert person_1_.first_name == 'Rich'
    assert person_1.city.name == 'Konoha'
    assert person_2_.first_name == 'Elton'
    assert person_2.city.name == 'Konoha'
    assert person_3_.first_name == 'Naruto'
    assert person_3.city.name == 'Konoha'


@async_decorator
async def test_save_contact():
    global contact_person_1
    global contact_person_2
    global contact_error
    # Creating instances of Contacts.
    contact_person_1 = Contact(phone="XXXXXXXXX-XXXX", id_person=person_1)
    contact_person_2 = Contact(phone="YYYYYYYYY-YYYY", id_person=person_2)
    contact_error = Contact(phone="YYYYYYYYY-YYYY", id_person=person_2)
    contact_person_1 = await Contact.save(contact_person_1)
    contact_person_2 = await Contact.save(contact_person_2)
    assert contact_person_1.phone == 'XXXXXXXXX-XXXX'
    assert contact_person_1.id_person.first_name == 'Rich'
    assert contact_person_2.phone == 'YYYYYYYYY-YYYY'
    assert contact_person_2.id_person.first_name == 'Elton'

    with pytest.raises(Exception):
        contact_error = await Contact.save(contact_error)


@async_decorator
async def test_drop_table():
    await Contact.drop_table()
    await Person.drop_table()
    await City.drop_table()
