from typing import Dict

from duck_orm.sql.sqlite import TYPES_SQL as TYPES_SQL_LITE
from duck_orm.sql.postgres import TYPES_SQL as TYPES_SQL_POSTGRES


class Column:
    def __init__(self, type_column: str, unique: bool = False,
                 primary_key: bool = False, not_null: bool = False,
                 auto_increment: bool = False):
        self.unique = unique
        self.primary_key = primary_key
        self.not_null = not_null
        self.type = type_column
        self.auto_increment = auto_increment

    def type_sql(self, dialect: str) -> str:
        column_sql = self.get_dialect(dialect)[self.type]
        return column_sql

    def column_sql(self, dialect: str) -> str:
        column_sql = self.get_dialect(dialect)[self.type]

        if (self.auto_increment and dialect == 'postgresql'):
            column_sql = "SERIAL"
        if (self.primary_key):
            column_sql += " PRIMARY KEY"
        if (self.auto_increment and dialect != 'postgresql'):
            column_sql += " AUTOINCREMENT"
        if (self.not_null):
            column_sql += " NOT NULL"
        if (self.unique):
            column_sql += " UNIQUE"

        return column_sql

    def get_dialect(self, dialect: str) -> Dict[str, str]:
        if dialect == 'postgresql':
            return TYPES_SQL_POSTGRES
        elif dialect == 'sqlite':
            return TYPES_SQL_LITE
        else:
            return TYPES_SQL_LITE


class String(Column, str):
    def __new__(cls, **kwargs):
        return super().__new__(cls, 'str')

    def __init__(self, min_length: int = 1, unique: bool = False,
                 primary_key: bool = False, not_null: bool = False):
        self.min_length = min_length
        super().__init__('str', unique, primary_key, not_null)


class Integer(Column, int):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, min_value: int = None, unique: bool = False,
                 primary_key: bool = False, auto_increment: bool = False,
                 not_null:  bool = False):
        self.min_value = min_value
        super().__init__('int', unique, primary_key,
                         auto_increment=auto_increment, not_null=not_null)


class BigInteger(Column, int):
    def __new__(cls, min_value: int = None, **kwargs):
        return super().__new__(cls)

    def __init__(self, min_value: int = None, unique: bool = False,
                 primary_key: bool = False):
        super().__init__('bigint', unique, primary_key)


class Varchar(Column, str):
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self, length: int, unique: bool = False,
                 primary_key: bool = False):
        self.length = length
        super().__init__('varchar', unique, primary_key)

    def column_sql(self, dialect: str):
        column_sql = super().column_sql(dialect)
        return column_sql.format(length=self.length)
