from duck_orm.sql.sql import QueryExecutor

SELECT_TABLES_SQL = "SELECT name FROM sqlite_master where type = 'table';"
SELECT_TABLE_SQL = "SELECT {fields} FROM {table};"
INSERT_INTO_SQL = "INSERT INTO {table}({fields_name}) VALUES({placeholders});"
CREATE_SQL = "CREATE TABLE IF NOT EXISTS {name} ({fields});"
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
