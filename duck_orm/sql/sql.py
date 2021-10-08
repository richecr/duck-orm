from typing import List, Mapping

SELECT_TABLES_SQL = "SELECT name FROM sqlite_master where type = 'table';"
SELECT_TABLE_SQL = "SELECT {fields} FROM {table} WHERE {conditions};"
SELECT_LIMIT_TABLE_SQL = "SELECT {fields} FROM {table} WHERE {conditions} " +\
    "LIMIT {limit};"
SELECT_ID_ORDER_BY_SQL = "SELECT {name_id} FROM {table} ORDER BY " +\
    "{name_id} DESC LIMIT 1;"
INSERT_INTO_SQL = "INSERT INTO {table}({fields_name}) VALUES({placeholders});"
CREATE_SQL = "CREATE TABLE IF NOT EXISTS {name} ({fields});"
UPDATE_SQL = "UPDATE {table} SET {fields_values} WHERE {conditions};"
DELETE_SQL = "DELETE FROM {table} WHERE {conditions};"
DROP_TABLE_SQL = "DROP TABLE {name};"

ALTER_TABLE_DROP_COLUMN = "ALTER TABLE {name_table} " + \
    "DROP COLUMN {field_name};"
ALTER_TABLE_ADD_CONSTRAINT_SQL = "ALTER TABLE {name_table} " + \
    "ADD CONSTRAINT {relation} " + \
    "FOREIGN KEY ({field_name}) " + \
    "REFERENCES {table_relation} ({field});"
ALTER_TABLE_ADD_COLUMN_SQL = "ALTER TABLE {name_table} ADD {name} {type_sql};"
ADD_FOREING_KEY_COLUMN_SQL = "FOREIGN KEY ({name}) REFERENCES {name_table} " +\
    "({name_in_table_fk}) ON DELETE {on_delete} ON UPDATE {on_update}"
CONSTRAINT_ADD_FOREING_KEY_COLUMN_SQL = "CONSTRAINT {name_constraint} " +\
    "FOREIGN KEY ({name}) REFERENCES {name_table} " +\
    "({name_in_table_fk}) ON DELETE {on_delete} ON UPDATE {on_update}"
ALTER_TABLE_ADD_COLUMN_WITH_CONSTRAINT_SQL = "ALTER TABLE {name_table} " + \
    "ADD COLUMN {field_name} {fields_type} " + \
    "REFERENCES {table_relation} ({field});"


class QueryExecutor:
    @classmethod
    def create_sql(cls, name_table: str, fields: List[str]):
        return CREATE_SQL.format(name=name_table, fields=", ".join(fields))

    @classmethod
    def insert_sql(
            cls,
            name_table: str,
            fields_name: List[str],
            placeholders: List[str]):
        return INSERT_INTO_SQL.format(table=name_table,
                                      fields_name=", ".join(fields_name),
                                      placeholders=", ".join(placeholders))

    @classmethod
    def update_sql(
            cls,
            name_table: str,
            fields_values: List[str],
            conditions: List[str]):
        return UPDATE_SQL.format(table=name_table,
                                 fields_values=", ".join(fields_values),
                                 conditions=", ".join(conditions))

    @classmethod
    def select_sql(
            cls,
            name_table: str,
            fields: List[str],
            conditions: str,
            limit: int = None):
        if (limit is not None):
            return SELECT_LIMIT_TABLE_SQL.format(
                limit=limit,
                table=name_table,
                fields=", ".join(fields),
                conditions=conditions)
        return SELECT_TABLE_SQL.format(
            table=name_table,
            fields=", ".join(fields),
            conditions=conditions)

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
    def alter_table_add_column_with_constraint(
        cls,
        name_table: str,
        field_name: str,
        table_relation: str,
        field: str,
        fields_type: str
    ):
        sql_add_column = ALTER_TABLE_ADD_COLUMN_WITH_CONSTRAINT_SQL.format(
            name_table=name_table,
            field_name=field_name,
            table_relation=table_relation,
            field=field,
            fields_type=fields_type
        )

        return sql_add_column

    @classmethod
    def alter_table_add_constraint(
        cls,
        name_table: str,
        relation: str,
        field_name: str,
        table_relation: str,
        field: str,
        fields_type: str = ''
    ):
        sqls: list[str] = []
        if fields_type:
            sql_remove_column = cls.alter_table_drop_column(
                name_table, field_name)
            sql_add_column = cls.alter_table_add_column_with_constraint(
                name_table, field_name, table_relation, field, fields_type)

            sqls += [sql_remove_column, sql_add_column]
        else:
            sql = ALTER_TABLE_ADD_CONSTRAINT_SQL.format(
                name_table=name_table,
                relation=relation,
                field_name=field_name,
                table_relation=table_relation,
                field=field)
            sqls += [sql]

        return sqls

    @classmethod
    def add_foreing_key_column(
        cls,
        name: str,
        name_table: str,
        name_in_table_fk: str,
        on_delete: str,
        on_update: str,
        name_constraint: str = ""
    ) -> str:
        args = {
            "name": name,
            "name_table": name_table,
            "name_in_table_fk": name_in_table_fk,
            "on_delete": on_delete,
            "on_update": on_update
        }
        if name_constraint != "":
            return CONSTRAINT_ADD_FOREING_KEY_COLUMN_SQL.format(
                **args, name_constraint=name_constraint)

        return ADD_FOREING_KEY_COLUMN_SQL.format(**args)

    @classmethod
    def alter_table_add_column(
        cls,
        name_table: str,
        name: str,
        type_sql: str
    ) -> str:
        return ALTER_TABLE_ADD_COLUMN_SQL.format(
            name_table=name_table,
            name=name,
            type_sql=type_sql
        )

    @classmethod
    def select_tables_sql(cls, name_table: str):
        return SELECT_TABLES_SQL

    @classmethod
    def alter_table_drop_column(cls, name_table: str, field_name: str):
        return ALTER_TABLE_DROP_COLUMN.format(
            name_table=name_table, field_name=field_name)

    @classmethod
    def parser(
            cls,
            row: Mapping,
            fields: List[str] = [],
            fields_foreign_key={}
    ) -> dict:
        entity = {}
        if (fields != []):
            for field in fields:
                if (row.__contains__(field)):
                    if field in fields_foreign_key.keys():
                        entity[field] = fields_foreign_key.get(field)
                    else:
                        entity[field] = row.get(field)
                else:
                    entity[field] = None
        else:
            for key, value in row.items():
                entity[key] = value

        return entity
