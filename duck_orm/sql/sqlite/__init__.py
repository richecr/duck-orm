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
ALTER_TABLE_ADD_CONSTRAINT_SQL = "ALTER TABLE {name_table} " + \
                                 "ADD COLUMN {field_name} {fields_type} " + \
                                 "REFERENCES {table_relation} ({field});"


class QuerySQLite(QueryExecutor):
    @classmethod
    def alter_table_add_constraint(
        self,
        name_table: str,
        relation: str,
        field_name: str,
        table_relation: str,
        field: str,
        fields_type: str
    ) -> str:
        return ALTER_TABLE_ADD_CONSTRAINT_SQL.format(
            name_table=name_table,
            field_name=field_name,
            table_relation=table_relation,
            field=field,
            fields_type=fields_type)
