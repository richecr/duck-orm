from typing import List
from duck_orm.sql.sql import QueryExecutor

SELECT_TABLES_SQL = "SELECT name FROM sqlite_master where type = 'table';"
SELECT_LIMIT_TABLE_SQL = "SELECT {fields} FROM {table} WHERE {conditions} LIMIT {limit};"
TYPES_SQL = {
    'str': 'TEXT',
    'int': 'INTEGER',
    'bigint': 'BIGINT',
    'float': 'FLOAT',
    'varchar': 'VARCHAR({length})',
    'char': 'CHARACTER({length})'
}


class QuerySQLite(QueryExecutor):
    @classmethod
    def select_sql(cls, name_table: str, fields: List[str], conditions: str, limit: int = None):
        if (limit != None):
            return SELECT_LIMIT_TABLE_SQL.format(limit=limit, table=name_table, fields=", ".join(fields), conditions=conditions)
        return SELECT_TABLE_SQL.format(table=name_table, fields=", ".join(fields), conditions=conditions)
