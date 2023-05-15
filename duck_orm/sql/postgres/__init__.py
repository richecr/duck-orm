from duck_orm.sql.sql import QueryExecutor

SELECT_TABLES_SQL = (
    "SELECT tablename " + "FROM pg_tables " + "WHERE schemaname = 'public';"
)
TYPES_SQL = {
    "str": "TEXT",
    "int": "INTEGER",
    "bigint": "BIGINT",
    "float": "FLOAT",
    "varchar": "VARCHAR({length})",
    "char": "CHARACTER({length})",
    "boolean": "BOOLEAN",
    "timestamp": "TIMESTAMP",
}


class QueryPostgres(QueryExecutor):
    @classmethod
    def select_tables_sql(cls):
        return SELECT_TABLES_SQL
