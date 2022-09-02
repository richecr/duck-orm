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
    url = '{}://{}'
    if dialect == 'sqlite3':
        url = '{}:///{}'
    db = Database(url.format(dialect, database_url))
    return db


model_manager = ModelManager()
db_connection = get_database()


class DuckORMMigrations(Model):
    __tablename__ = 'duckorm_migrations'
    __db__ = db_connection
    model_manager = model_manager

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    name: str = Field.String()
    migration_time: datetime = Field.Timestamp()


async def create_table_migration():
    await db_connection.connect()
    tables = await DuckORMMigrations.find_all_tables()
    has_tb_migrations = False
    for table in tables:
        if 'duckorm_migrations' in list(table.values()):
            has_tb_migrations = True

    if not has_tb_migrations:
        await DuckORMMigrations.create()
    await db_connection.disconnect()


async def execute_up_migration(migration):
    await db_connection.connect()
    await migration.up(model_manager)
    await db_connection.disconnect()


async def execute_down_migration(migration):
    await db_connection.connect()
    await migration.down(model_manager)
    await db_connection.disconnect()


async def has_migration_executed(name_migration):
    await db_connection.connect()
    has_duck_migration = await DuckORMMigrations.find_one(conditions=[Condition('name', '=', name_migration)])
    await db_connection.disconnect()
    return has_duck_migration is None


async def save_migration(name_migration):
    await db_connection.connect()
    await DuckORMMigrations.save(DuckORMMigrations(name=name_migration, migration_time=datetime.now()))
    await db_connection.disconnect()


async def find_all_migrations():
    await db_connection.connect()
    migrations_tables = await DuckORMMigrations.find_all()
    await db_connection.disconnect()
    return migrations_tables


async def delete_migrations(migration_names: list[str]):
    await db_connection.connect()
    await DuckORMMigrations.delete(conditions=[Condition('name', 'IN', migration_names)])
    await db_connection.disconnect()
