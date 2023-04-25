import logging

from duck_orm.sql.sql import QueryExecutor
from duck_orm.sql.sqlite import QuerySQLite
from duck_orm.sql.postgres import QueryPostgres


def get_dialect(dialect: str) -> QueryExecutor:
    if dialect == 'postgresql':
        return QueryPostgres()
    elif dialect == 'sqlite':
        return QuerySQLite()

    raise Exception(f"Dialect {dialect} not supported!")


def load_path(dir_migration):
    from importlib.machinery import SourceFileLoader
    return SourceFileLoader('module.name', dir_migration).load_module()


def log_info(msg):
    print(msg)
    logging.info(msg)


def log_error(msg):
    print(msg)
    logging.error(msg)
