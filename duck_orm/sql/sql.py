from typing import List, Mapping

SELECT_TABLES_SQL = "SELECT name FROM sqlite_master where type = 'table';"
SELECT_TABLE_SQL = "SELECT {fields} FROM {table};"
INSERT_INTO_SQL = "INSERT INTO {table}({fields_name}) VALUES({placeholders});"
CREATE_SQL = "CREATE TABLE IF NOT EXISTS {name} ({fields});"
DROP_TABLE_SQL = "DROP TABLE {name};"


class QueryExecutor:
    @classmethod
    def create_sql(cls, name_table: str, fields: List[str]):
        return CREATE_SQL.format(name=name_table, fields=", ".join(fields))

    @classmethod
    def insert_sql(cls, name_table: str, fields_name: List[str], placeholders: List[str]):
        return INSERT_INTO_SQL.format(table=name_table,
                                      fields_name=", ".join(fields_name),
                                      placeholders=", ".join(placeholders))

    @classmethod
    def select_sql(cls, name_table: str, fields: List[str]):
        return SELECT_TABLE_SQL.format(table=name_table, fields=", ".join(fields))

    @classmethod
    def drop_table(cls, name_table: str):
        return DROP_TABLE_SQL.format(name=name_table)

    @classmethod
    def select_tables_sql(cls, name_table: str):
        return SELECT_TABLES_SQL

    @classmethod
    def parser(cls, row: Mapping):
        entity = {}
        for key, value in row.items():
            entity[key] = value

        return entity
