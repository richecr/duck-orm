import os
import typer
import shutil
from datetime import datetime
from asyncio import run as aiorun
from databases.core import Database

from duck_orm.model import Model
from duck_orm.model_manager import ModelManager
from duck_orm.sql import fields as Field
from duck_orm.sql.condition import Condition
from duck_orm.utils.functions import log_info, log_error

app = typer.Typer()
model_manager = ModelManager()


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


db_connection = get_database()


class DuckORMMigrations(Model):
    __tablename__ = 'duckorm_migrations'
    __db__: Database = db_connection
    model_manager = model_manager

    id: int = Field.Integer(primary_key=True, auto_increment=True)
    name: str = Field.String()
    migration_time: datetime = Field.Timestamp()


@app.command()
def init():
    code = """configs = {
    'development': {
        'client': 'postgresql',
        'database_url': 'url',
    },
    'production': {
        'client': 'postgresql',
        'database_url': 'url',
    }
}
"""
    with open('./duckorm_file.py', 'w') as file:
        file.writelines(code)
        print('File configuration created!')

    if not os.path.exists('./migrations'):
        os.mkdir('./migrations')
        print('Folder migrations created!')

    if not os.path.exists('./seeds'):
        os.mkdir('./seeds')
        print('Folder seeds created!')

    log_info('DuckORM started.')


@app.command()
def create_migrate(name: str):
    code = """from duck_orm.sql import fields as Field
from duck_orm.model_manager import ModelManager


async def up(model_manager: ModelManager):
    await model_manager.create_table('users', {
        'id': Field.Integer(primary_key=True, auto_increment=True),
        'name': Field.String(),
        'email': Field.String(unique=True)
    })


async def down(model_manager: ModelManager):
    await model_manager.drop_table('users')
"""
    if not os.path.exists('./migrations'):
        log_error('Error: Run command init!')

    if '-' in name:
        log_error('Invalid characters. Type: create_users and not create-users.')
    else:
        time_ms = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        filename = str(time_ms) + '_' + name
        with open('./migrations/{}.py'.format(filename), 'w') as file:
            file.writelines(code)
            log_info('Migration {} created successfully.'.format(filename))


@app.command()
def run_migrations():
    async def _create_table_migrations():
        await db_connection.connect()
        tables = await DuckORMMigrations.find_all_tables()
        has_tb_migrations = False
        for table in tables:
            if list(table.values())[0] == 'duckorm_migrations':
                has_tb_migrations = True

        if not has_tb_migrations:
            await DuckORMMigrations.create()
        await db_connection.disconnect()

    def get_name_to_migration(path_migration: str):
        return path_migration.split('migrations/')[-1]

    async def _run_migrations():
        dir = './migrations/'
        directory = os.listdir(dir)
        migrations = [os.path.join(dir, nome) for nome in directory]

        for migration in migrations:
            name_migration = get_name_to_migration(migration)
            await db_connection.connect()
            has_duck_migration = await DuckORMMigrations.find_one(conditions=[
                Condition('name', '=', name_migration)]
            )
            if has_duck_migration is None:
                from importlib.machinery import SourceFileLoader
                file = SourceFileLoader('module.name', migration).load_module()
                await file.up(model_manager)
                duck_migration = DuckORMMigrations(
                    name=name_migration, migration_time=datetime.now())
                await DuckORMMigrations.save(duck_migration)
            await db_connection.disconnect()

            log_info('Migration {} performed successfully.'.format(name_migration))

            if os.path.exists('./migrations/__pycache__'):
                shutil.rmtree('./migrations/__pycache__')

    aiorun(_create_table_migrations())
    aiorun(_run_migrations())


@app.command()
def undo_migrations():
    def get_name_to_migration(path_migration: str):
        return path_migration.split('migrations/')[-1]

    async def _undo_migrations():
        dir = './migrations/'
        directory = os.listdir(dir)
        migrations = reversed([os.path.join(dir, nome) for nome in directory])
        model_manager = ModelManager()

        for migration in migrations:
            name_migration = get_name_to_migration(migration)
            conditions = [Condition('name', '=', name_migration)]
            await db_connection.connect()
            has_duck_migration = await DuckORMMigrations.find_one(conditions=conditions)
            if has_duck_migration is not None:
                from importlib.machinery import SourceFileLoader
                file = SourceFileLoader('module.name', migration).load_module()
                await file.down(model_manager)
                await DuckORMMigrations.delete(conditions=conditions)
            await db_connection.disconnect()

            log_info('Undo Migration {} performed successfully.'.format(
                name_migration))

            if os.path.exists('./migrations/__pycache__'):
                shutil.rmtree('./migrations/__pycache__')

    aiorun(_undo_migrations())


@app.command()
def create_seed(name: str):
    code = """from duck_orm import duck_orm
from duck_orm.sql.condition import Condition


def up():
    return duck_orm.insert('users', [
        {
            'id': 1,
            'name': 'User 1',
            'email': 'user1@gmail.com'
        }
    ])


def down():
    return duck_orm.remove('users', conditions=[
            Condition('id', '=', 1)
        ])
"""
    if not os.path.exists('./seeds'):
        log_error('Error: Run command init!')

    if '-' in name:
        log_error('Invalid characters. Type: create_users and not create-users.')
    else:
        time_ms = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        filename = name + '-' + str(time_ms)
        with open('./seeds/{}.py'.format(filename), 'w') as file:
            file.writelines(code)
            log_info('Seed {} performed successfully.'.format(filename))


if __name__ == "__main__":
    app()
