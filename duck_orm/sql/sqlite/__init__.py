from datetime import datetime
from typing import List, Mapping

from duck_orm.sql.sql import QueryExecutor

SELECT_TABLES_SQL = "SELECT name FROM sqlite_master where type = 'table';"
DROP_TABLE_SQL = "DROP TABLE IF EXISTS {name};"
TYPES_SQL = {
    "str": "TEXT",
    "int": "INTEGER",
    "bigint": "BIGINT",
    "float": "FLOAT",
    "varchar": "VARCHAR({length})",
    "char": "CHARACTER({length})",
    "boolean": "INTEGER",
    "timestamp": "TEXT",
}


class QuerySQLite(QueryExecutor):
    @classmethod
    def drop_table(cls, name_table: str, cascade: bool = False):
        return DROP_TABLE_SQL.format(name=name_table)

    @classmethod
    def parser(cls, row: Mapping, fields: List[str] = [], fields_foreign_key={}) -> dict:
        entity = {}
        if fields != []:
            for field in fields:
                field_type = None
                if isinstance(field, tuple):
                    field = field[0]
                    field_type = field[1]

                try:
                    value = row[field]
                    if value is not None:
                        if field_type:
                            entity[field] = datetime.strptime(value, "%Y-%m-%d %H:%M:%S.%f")
                        elif field in fields_foreign_key.keys():
                            entity[field] = fields_foreign_key.get(field)
                        else:
                            entity[field] = value
                    elif fields_foreign_key.__contains__(field):
                        entity[field] = fields_foreign_key[field]
                    else:
                        entity[field] = None
                except KeyError:
                    entity[field] = None

        else:
            for key, value in row.items():
                entity[key] = value
        return entity
