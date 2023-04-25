from datetime import datetime
from databases.core import Database

from duck_orm.model import Model
from duck_orm.model_manager import ModelManager
from duck_orm.sql.condition import Condition
from duck_orm.sql import fields as Field


def get_database():
    from importlib.machinery import SourceFileLoader
    file = SourceFileLoader('module.name', './duckorm_file.py').load_module()
    configs = file.configs
    dialect = configs['development']['client']
    database_url = configs['development']['database_url']
    url = '{}:///{}' if dialect == 'sqlite3' else '{}://{}'
    return Database(url.format(dialect, database_url))


model_manager = ModelManager()
db_connection = get_database()


class DuckORMSeeds(Model):
    __tablename__ = 'duckorm_seeds'
    __db__ = db_connection
    model_manager = model_manager

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    name: str = Field.String()
    seed_time: datetime = Field.Timestamp()


async def create_table_seed():
    await db_connection.connect()
    tables = await DuckORMSeeds.find_all_tables()
    has_tb_seeds = False
    for table in tables:
        if 'duckorm_seeds' in list(table.values()):
            has_tb_seeds = True

    if not has_tb_seeds:
        await DuckORMSeeds.create()
    await db_connection.disconnect()


async def execute_up_seed(seed):
    await db_connection.connect()
    await seed.up(model_manager)
    await db_connection.disconnect()


async def execute_down_seed(seed):
    await db_connection.connect()
    await seed.down(model_manager)
    await db_connection.disconnect()


async def has_seed_executed(name_seed):
    await db_connection.connect()
    has_duck_seed = await DuckORMSeeds.find_one(conditions=[Condition('name', '=', name_seed)])
    await db_connection.disconnect()
    return has_duck_seed is None


async def save_seed(name_seed):
    await db_connection.connect()
    await DuckORMSeeds.save(DuckORMSeeds(name=name_seed, seed_time=datetime.now()))
    await db_connection.disconnect()


async def find_all_seeds():
    await db_connection.connect()
    seeds_tables = await DuckORMSeeds.find_all()
    await db_connection.disconnect()
    return seeds_tables


async def delete_seeds(seed_names: list[str]):
    await db_connection.connect()
    await DuckORMSeeds.delete(conditions=[Condition('name', 'IN', seed_names)])
    await db_connection.disconnect()
