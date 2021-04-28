from typing import List
from duck_orm.sql.sql import QueryExecutor

SELECT_TABLES_SQL = "SELECT name FROM sqlite_master where type = 'table';"
TYPES_SQL = {
    'str': 'TEXT',
    'int': 'INTEGER',
    'bigint': 'BIGINT',
    'float': 'FLOAT',
    'varchar': 'VARCHAR({length})',
    'char': 'CHARACTER({length})'
}


class QuerySQLite(QueryExecutor):
    pass
