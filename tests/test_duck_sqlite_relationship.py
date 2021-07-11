from databases.core import Database
import functools
import asyncio
import pytest

from duck_orm.model import Model
from duck_orm.sql import fields as Field
from duck_orm.sql.relationship import ForeignKey, ManyToMany, ManyToOne, OneToOne, OneToMany

db = Database('sqlite:///example.db')


class City(Model):
    __tablename__ = 'cities'
    __db__ = db

    id: int = Field.Integer(
        primary_key=True,
        auto_increment=True)
    name: str = Field.String(unique=True)

    def relationships(self):
        self.persons = OneToMany(
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
    city: City = ForeignKey(model=City, name_in_table_fk='id')


class Contact(Model):
    __tablename__ = 'contacts'
    __db__ = db

    id_person = OneToOne(
        model=Person,
        name_relation='person_contact',
        field='id_person')
    phone: str = Field.String(not_null=True)


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
    assert Contact.get_name() == 'contacts'
    assert User.get_name() == 'users'
    assert WorkingDay.get_name() == 'working_days'
    assert UsersWorkingDay.get_name() == 'users_working_days'
    assert isinstance(Person.city, ForeignKey)
    assert isinstance(UsersWorkingDay.users, ForeignKey)
    assert isinstance(UsersWorkingDay.working_days, ForeignKey)


def test_create_sql():
    sql = Person._Model__get_create_sql()
    assert sql == "CREATE TABLE IF NOT EXISTS persons (" + \
        "salary BIGINT, " + \
        "last_name TEXT NOT NULL, " + \
        "id_teste INTEGER PRIMARY KEY AUTOINCREMENT, " + \
        "first_name TEXT UNIQUE, " + \
        "city INTEGER, " + \
        "age BIGINT, " + \
        " FOREIGN KEY (city) REFERENCES cities (id));"


def get_table(table, tables):
    for tup in tables:
        if (tup['name'] == table):
            return True
    return False


@async_decorator
async def test_create_table():
    await db.connect()
    await City.create()
    await Person.create()
    await Contact.create()
    await User.create()
    await WorkingDay.create()
    await UsersWorkingDay.create()

    # await City.associations()
    # await Person.associations()
    # await Contact.associations()
    # await User.associations()
    # await WorkingDay.associations()
    # await UsersWorkingDay.associations()

    tables = await Person.find_all_tables()
    assert get_table('persons', tables)
    assert get_table('contacts', tables)
    assert get_table('cities', tables)
    assert get_table('users', tables)
    assert get_table('working_days', tables)
    assert get_table('users_working_days', tables)


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
async def test_save_users():
    global user, user1, user2

    user = User(name='Rich')
    user1 = User(name='Rich 1')
    user2 = User(name='Rich 2')

    user = await User.save(user)
    user1 = await User.save(user1)
    user2 = await User.save(user2)
    assert user.id == 1
    assert user.name == 'Rich'
    assert user1.id == 2
    assert user1.name == 'Rich 1'
    assert user2.id == 3
    assert user2.name == 'Rich 2'


@async_decorator
async def test_save_working_days():
    global working_day, working_day1, working_day2

    working_day = WorkingDay(week_day='segunda', working_date='17/05/1999')
    working_day1 = WorkingDay(week_day='segunda 1', working_date='17/06/1999')
    working_day2 = WorkingDay(week_day='segunda 2', working_date='17/07/1999')
    working_day = await WorkingDay.save(working_day)
    working_day1 = await WorkingDay.save(working_day1)
    working_day2 = await WorkingDay.save(working_day2)
    assert working_day.id == 1
    assert working_day.week_day == 'segunda'
    assert working_day.working_date == '17/05/1999'
    assert working_day1.id == 2
    assert working_day1.week_day == 'segunda 1'
    assert working_day1.working_date == '17/06/1999'
    assert working_day2.id == 3
    assert working_day2.week_day == 'segunda 2'
    assert working_day2.working_date == '17/07/1999'


@async_decorator
async def test_save_users_working_days():
    await User.working_day.add_models(working_day, user)
    await User.working_day.add_models(working_day, user1)
    await User.working_day.add_models(working_day, user2)
    await user.working_day.add(working_day1)
    await user.working_day.add(working_day2)

    working_days: list[WorkingDay] = await user.working_day.get_all()
    assert len(working_days) == 3
    assert working_days[0].id == 1
    assert working_days[0].week_day == 'segunda'
    assert working_days[1].id == 2
    assert working_days[1].week_day == 'segunda 1'
    assert working_days[2].id == 3
    assert working_days[2].week_day == 'segunda 2'


@async_decorator
async def test_drop_table():
    await Contact.drop_table()
    await Person.drop_table()
    await City.drop_table()
    await UsersWorkingDay.drop_table()
    await WorkingDay.drop_table()
    await User.drop_table()
