import os
import typer
import shutil
from datetime import datetime
from asyncio import run as aiorun

from duck_orm.model_manager import ModelManager

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
        print("File configuration created!")

    if not os.path.exists('./migrations'):
        os.mkdir('./migrations')
        print("Folder migrations created!")

    if not os.path.exists('./seeds'):
        os.mkdir('./seeds')
        print("Folder seeds created!")


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
        print('Error: Run command init!')

    if '-' in name:
        print('Invalid characters. Type: create_users and not create-users.')
    else:
        time_ms = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        filename = str(time_ms) + '_' + name
        with open('./migrations/{}.py'.format(filename), 'w') as file:
            file.writelines(code)
            print("Migration created!")


@app.command()
def run_migrations():
    async def _run_migrations():
        dir = './migrations/'
        directory = os.listdir(dir)
        migrations = [os.path.join(dir, nome) for nome in directory]
        model_manager = ModelManager()
        for migration in migrations:
            from importlib.machinery import SourceFileLoader
            file = SourceFileLoader("module.name", migration).load_module()
            await file.up(model_manager)
            if os.path.exists('./migrations/__pycache__'):
                shutil.rmtree('./migrations/__pycache__')

    aiorun(_run_migrations())


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
        print('Error: Run command init!')

    if '-' in name:
        print('Invalid characters. Type: create_users and not create-users.')
    else:
        time_ms = datetime.utcnow().strftime('%Y%m%d%H%M%S%f')
        filename = name + '-' + str(time_ms)
        with open('./seeds/{}.py'.format(filename), 'w') as file:
            file.writelines(code)
            print("Seed created!")


if __name__ == "__main__":
    app()
