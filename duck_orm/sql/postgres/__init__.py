from duck_orm.sql.sql import QueryExecutor

SELECT_TABLES_SQL = "SELECT tablename FROM pg_tables where schemaname = 'public';"
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


class QueryPostgres(QueryExecutor):
    @classmethod
    def select_tables_sql(cls, name_table: str):
        return SELECT_TABLES_SQL
