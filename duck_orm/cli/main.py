import os
import typer
import shutil
from datetime import datetime
from datetime import timezone
from asyncio import run as aiorun

from duck_orm.utils.functions import load_path, log_info, log_error

app = typer.Typer()


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
    if not os.path.exists('./migrations'):
        log_error('Error: Run command init!')

    if '-' in name:
        log_error('Invalid characters. Type: create_users and not create-users.')
    else:
        time_ms = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')
        filename = f'{str(time_ms)}_{name}'
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
        with open(f'./migrations/{filename}.py', 'w') as file:
            file.writelines(code)
            log_info(f'Migration {filename} created successfully.')


@app.command()
def run_migrations():
    from model_migration import (
        has_migration_executed, save_migration, create_table_migration, execute_up_migration)

    def get_name_to_migration(path_migration: str):
        return path_migration.split('migrations/')[-1]

    async def _run_migrations():
        directory = os.listdir(dir)
        migrations = [os.path.join('./migrations/', nome) for nome in directory]

        for migration in migrations:
            name_migration = get_name_to_migration(migration)
            if await has_migration_executed(name_migration):
                file = load_path(migration)
                await execute_up_migration(file)
                await save_migration(name_migration)

            log_info('Migration {} performed successfully.'.format(name_migration))
            if os.path.exists('./migrations/__pycache__'):
                shutil.rmtree('./migrations/__pycache__')

    aiorun(create_table_migration())
    aiorun(_run_migrations())


@app.command()
def undo_migrations_all():
    async def _undo_migrations():
        from model_migration import (
            execute_down_migration, find_all_migrations, delete_migrations)

        migrations_tables = await find_all_migrations()
        migration_names: list[str] = []
        for migration in migrations_tables:
            file = load_path(load_path(f'./migrations/{migration.name}'))
            await execute_down_migration(file)
            migration_names.append(migration.name)
            log_info('Undo Migration {} performed successfully.'.format(migration.name))
            if os.path.exists('./migrations/__pycache__'):
                shutil.rmtree('./migrations/__pycache__')

        await delete_migrations(migration_names)

    aiorun(_undo_migrations())


@app.command()
def create_seed(name: str):
    if not os.path.exists('./seeds'):
        log_error('Error: Run command init!')

    if '-' in name:
        log_error('Invalid characters. Type: create_users and not create-users.')
    else:
        time_ms = datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S%f')
        filename = f'{name}-{str(time_ms)}'
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
        with open(f'./seeds/{filename}.py', 'w') as file:
            file.writelines(code)
            log_info(f'Seed {filename} performed successfully.')


if __name__ == "__main__":
    app()
