from databases.core import Database
import functools
import asyncio
import pytest

from duck_orm.Model import Model
from duck_orm.sql import fields as Field
from duck_orm.sql.Condition import Condition

db = Database('sqlite:///example.db')


class Person(Model):
    __tablename__ = 'persons'
    __db__ = db

    id: int = Field.Integer(
        primary_key=True, auto_increment=True, not_null=True)
    first_name: str = Field.String(unique=True)
    last_name: str = Field.String(not_null=True)
    age: int = Field.Integer(min_value=18)
    salary: int = Field.BigInteger()


@pytest.fixture(autouse=True)
async def create_test_database():
    await db.connect()
    yield
    await Person.drop_table()


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
    assert Person._get_name() == 'persons'
    assert isinstance(Person.first_name, Field.String)
    assert issubclass(Person, Model)


def test_create_sql():
    sql = Person._get_create_sql()
    print(sql)
    assert sql == "CREATE TABLE IF NOT EXISTS persons (" + \
        "age INTEGER, " + \
        "first_name TEXT UNIQUE, " + \
        "id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, " + \
        "last_name TEXT NOT NULL, " + \
        "salary BIGINT);"


def get_table(table, tables):
    for tup in tables:
        if (tup['name'] == table):
            return True
    return False


@async_decorator
async def test_create_table():
    await Person.create()
    tables = await Person.find_all_tables()
    assert get_table('persons', tables)


@async_decorator
async def test_save_person():
    p = Person(first_name="Rich", last_name="Rich Ramalho",
               age=21, salary=10000000)
    await p.save(p)
    persons = await Person.find_all(['first_name'])
    assert persons[0].first_name == 'Rich'


@async_decorator
async def test_select_all_persons():
    p = Person(first_name="Lucas", last_name="Lucas Andrade",
               age=21, salary=20000000)
    await p.save(p)
    persons = await Person.find_all(['first_name'])
    assert persons[0].first_name == 'Lucas'
    assert persons[1].first_name == 'Rich'


@async_decorator
async def test_sql_select_where_persons():
    sql = Person._get_select_sql(
        conditions=[
            Condition('first_name', '=', 'Rich')
        ]
    )
    assert sql[0] == "SELECT id, age, first_name, id, last_name, salary FROM persons WHERE first_name = 'Rich';"


@async_decorator
async def test_select_where_persons():
    persons = await Person.find_all(
        conditions=[
            Condition('first_name', '=', 'Rich')
        ]
    )
    assert len(persons) == 1
    assert persons[0].first_name == 'Rich'


@async_decorator
async def test_delete_person():
    await Person.delete(
        conditions=[
            Condition('first_name', '=', 'Rich')
        ]
    )
    persons = await Person.find_all()
    print(persons)
    assert len(persons) == 1
    assert persons[0].first_name == 'Lucas'


@async_decorator
async def test_find_one():
    person = await Person.find_one(conditions=[
        Condition('first_name', '=', 'Lucas')
    ])
    assert person != None
    assert person.first_name == 'Lucas'
    assert person.last_name == 'Lucas Andrade'


@async_decorator
async def test_find_one_not_found():
    person = await Person.find_one(conditions=[
        Condition('first_name', '=', 'Rich')
    ])
    assert person == None


@async_decorator
async def test_drop_table():
    await Person.drop_table()
