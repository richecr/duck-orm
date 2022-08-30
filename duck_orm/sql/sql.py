from typing import List, Mapping

SELECT_TABLES_SQL = "SELECT name FROM sqlite_master where type = 'table';"
SELECT_TABLE_SQL = "SELECT {fields} FROM {table}"
LIMIT_SQL = " LIMIT {limit}"
ORDER_BY_SQL = " ORDER BY {name_id} DESC"
SELECT_TABLE_WHERE_SQL = SELECT_TABLE_SQL + " WHERE {conditions}"
SELECT_LAST_ID_ORDER_BY_SQL = "SELECT {name_id} FROM {table} " +\
    ORDER_BY_SQL + " LIMIT 1;"

INSERT_INTO_SQL = "INSERT INTO {table}({fields_name}) VALUES({placeholders});"
CREATE_SQL = "CREATE TABLE IF NOT EXISTS {name} ({fields});"
UPDATE_SQL = "UPDATE {table} SET {fields_values} WHERE {conditions};"
DELETE_SQL = "DELETE FROM {table} WHERE {conditions};"
DROP_TABLE_SQL = "DROP TABLE IF EXISTS {name}"

ADD_COLUMN_SQL = "ALTER TABLE {table_name} " + \
    "ADD COLUMN {field_name} {field_type} "

ADD_FK_SQL = "REFERENCES {table_relation} ({field}) " + \
    "ON DELETE {on_delete} ON UPDATE {on_update}"

ADD_FK_COLUMN_SQL = "FOREIGN KEY ({name}) " + ADD_FK_SQL

ADD_FK_WITH_CONSTRAINT_WITHOUT_ALTER_SQL = "CONSTRAINT {name_constraint} " + \
    ADD_FK_COLUMN_SQL

ADD_FK_WITH_CONSTRAINT_SQL = "CONSTRAINT {name_constraint} " + ADD_FK_SQL

ADD_COLUMN_FK_WITH_CONSTRAINT_SQL = ADD_COLUMN_SQL + ADD_FK_WITH_CONSTRAINT_SQL
ADD_COLUMN_FK_SQL = ADD_COLUMN_SQL + ADD_FK_SQL


class QueryExecutor:
    @classmethod
    def create_sql(cls, name_table: str, fields: List[str]):
        return CREATE_SQL.format(name=name_table, fields=", ".join(fields))

    @classmethod
    def insert_sql(
            cls,
            name_table: str,
            fields_name: List[str],
            placeholders: List[str]
    ):
        return INSERT_INTO_SQL.format(table=name_table,
                                      fields_name=", ".join(fields_name),
                                      placeholders=", ".join(placeholders))

    @classmethod
    def update_sql(
            cls,
            name_table: str,
            fields_values: List[str],
            conditions: List[str]
    ):
        return UPDATE_SQL.format(table=name_table,
                                 fields_values=", ".join(fields_values),
                                 conditions=", ".join(conditions))

    @classmethod
    def select_sql(
            cls,
            name_table: str,
            fields: List[str],
            conditions: str,
            limit: int = None
    ) -> str:
        sql = SELECT_TABLE_WHERE_SQL
        if (limit is not None):
            sql += LIMIT_SQL

        return sql.format(
            table=name_table,
            fields=", ".join(fields),
            conditions=conditions,
            limit=limit
        )

    @classmethod
    def select_last_id(cls, name_id: str, table: str):
        return SELECT_LAST_ID_ORDER_BY_SQL.format(name_id=name_id, table=table)

    @classmethod
    def delete_sql(cls, name_table: str, conditions: str):
        return DELETE_SQL.format(table=name_table, conditions=conditions)

    @classmethod
    def drop_table(cls, name_table: str, cascade: bool = False):
        sql = DROP_TABLE_SQL.format(name=name_table)
        if cascade:
            sql += " CASCADE;"

        return sql

    @classmethod
    def alter_table_add_column_with_constraint(
        cls,
        table_name: str,
        field_name: str,
        table_relation: str,
        field: str,
        field_type: str,
        on_delete: str,
        on_update: str,
        name_constraint: str = ''
    ) -> str:
        args = {
            "table_name": table_name,
            "field_name": field_name,
            "table_relation": table_relation,
            "field": field,
            "field_type": field_type,
            "on_delete": on_delete,
            "on_update": on_update
        }
        if name_constraint != "":
            return ADD_COLUMN_FK_WITH_CONSTRAINT_SQL.format(
                **args, name_constraint=name_constraint)

        return ADD_COLUMN_FK_SQL.format(**args)

    @classmethod
    def add_foreing_key_column(
        cls,
        name: str,
        table_name: str,
        field: str,
        on_delete: str,
        on_update: str,
        name_constraint: str = ""
    ) -> str:
        args = {
            "name": name,
            "table_relation": table_name,
            "field": field,
            "on_delete": on_delete,
            "on_update": on_update
        }
        if name_constraint != "":
            return ADD_FK_WITH_CONSTRAINT_WITHOUT_ALTER_SQL.format(
                **args, name_constraint=name_constraint)

        return ADD_FK_COLUMN_SQL.format(**args)

    @classmethod
    def select_tables_sql(cls):
        return SELECT_TABLES_SQL

    @classmethod
    def parser(
            cls,
            row: Mapping,
            fields: List[str] = [],
            fields_foreign_key: dict = {}
    ) -> dict:
        entity = {}
        if (fields != []):
            for field in fields:
                if isinstance(field, tuple):
                    field = field[0]

                if (row.__contains__(field)):
                    if fields_foreign_key.__contains__(field):
                        entity[field] = fields_foreign_key.get(field)
                    else:
                        entity[field] = row.get(field)
                elif fields_foreign_key.__contains__(field):
                    entity[field] = fields_foreign_key[field]
                else:
                    entity[field] = None
        else:
            for key, value in row.items():
                entity[key] = value

        return entity
