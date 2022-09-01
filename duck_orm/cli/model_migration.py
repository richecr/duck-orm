from datetime import datetime
from databases.core import Database

from duck_orm.model import Model
from duck_orm.model_manager import ModelManager
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
