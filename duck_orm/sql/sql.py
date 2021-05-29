from typing import List, Mapping

SELECT_TABLES_SQL = "SELECT name FROM sqlite_master where type = 'table';"
SELECT_TABLE_SQL = "SELECT {fields} FROM {table} WHERE {conditions};"
SELECT_LIMIT_TABLE_SQL = "SELECT {fields} FROM {table} WHERE {conditions} LIMIT {limit};"
SELECT_ID_ORDER_BY_SQL = "SELECT {name_id} FROM {table} ORDER BY {name_id} DESC LIMIT 1;"
INSERT_INTO_SQL = "INSERT INTO {table}({fields_name}) VALUES({placeholders});"
CREATE_SQL = "CREATE TABLE IF NOT EXISTS {name} ({fields});"
UPDATE_SQL = "UPDATE {table} SET {fields_values} WHERE {conditions};"
DELETE_SQL = "DELETE FROM {table} WHERE {conditions};"
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
    def update_sql(cls, name_table: str, fields_values: List[str], conditions: List[str]):
        return UPDATE_SQL.format(table=name_table,
                                 fields_values=", ".join(fields_values),
                                 conditions=", ".join(conditions))

    @classmethod
    def select_sql(cls, name_table: str, fields: List[str], conditions: str, limit: int = None):
        if (limit != None):
            return SELECT_LIMIT_TABLE_SQL.format(limit=limit, table=name_table, fields=", ".join(fields), conditions=conditions)
        return SELECT_TABLE_SQL.format(table=name_table, fields=", ".join(fields), conditions=conditions)

    @classmethod
    def select_last_id(cls, name_id: str, table: str):
        return SELECT_ID_ORDER_BY_SQL.format(name_id=name_id, table=table)

    @classmethod
    def delete_sql(cls, name_table: str, conditions: str):
        return DELETE_SQL.format(table=name_table, conditions=conditions)

    @classmethod
    def drop_table(cls, name_table: str):
        return DROP_TABLE_SQL.format(name=name_table)

    @classmethod
    def select_tables_sql(cls, name_table: str):
        return SELECT_TABLES_SQL

    @classmethod
    def parser(cls, row: Mapping, fields: List[str] = []):
        entity = {}
        row = dict(row.items())
        if (fields != []):
            for field in fields:
                if (row.__contains__(field)):
                    entity[field] = row.get(field)
                else:
                    entity[field] = None
        else:
            for key, value in row.items():
                entity[key] = value

        return entity
