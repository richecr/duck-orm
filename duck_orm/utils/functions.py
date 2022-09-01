import picologging as logging

from duck_orm.sql.sql import QueryExecutor
from duck_orm.sql.sqlite import QuerySQLite
from duck_orm.sql.postgres import QueryPostgres


def get_dialect(dialect: str) -> QueryExecutor:
    if dialect == 'postgresql':
        return QueryPostgres()
    elif dialect == 'sqlite':
        return QuerySQLite()

    raise Exception("Dialect {} not supported!".format(dialect))


def log_info(msg):
    print(msg)
    logging.info(msg)


def log_error(msg):
    print(msg)
    logging.error(msg)
