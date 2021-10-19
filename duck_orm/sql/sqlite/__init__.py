from duck_orm.sql.sql import QueryExecutor

SELECT_TABLES_SQL = "SELECT name FROM sqlite_master where type = 'table';"
DROP_TABLE_SQL = "DROP TABLE {name};"
TYPES_SQL = {
    'str': 'TEXT',
    'int': 'INTEGER',
    'bigint': 'BIGINT',
    'float': 'FLOAT',
    'varchar': 'VARCHAR({length})',
    'char': 'CHARACTER({length})',
    'boolean': 'INTEGER'
}


class QuerySQLite(QueryExecutor):
    @classmethod
    def drop_table(cls, name_table: str, cascade: bool = False):
        return DROP_TABLE_SQL.format(name=name_table)
