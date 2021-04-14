from duck_orm.sql.sql import QueryExecutor

SELECT_TABLES_SQL = "SELECT tablename FROM pg_tables where schemaname = 'public';"
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
