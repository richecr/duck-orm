from typing import Dict
from enum import Enum

from duck_orm.sql.sqlite import TYPES_SQL as TYPES_SQL_LITE
from duck_orm.sql.postgres import TYPES_SQL as TYPES_SQL_POSTGRES


class ActionsEnum(Enum):
    NO_ACTION = "NO ACTION"
    RESTRICT = "RESTRICT"
    CASCADE = "CASCADE"
    SET_DEFAULT = "SET DEFAULT"
    SET_NULL = "SET NULL"


class Column:
    def __init__(self, type_column: str, unique: bool = False,
                 primary_key: bool = False, not_null: bool = False,
                 auto_increment: bool = False, default_value=None):
        self.unique = unique
        self.primary_key = primary_key
        self.not_null = not_null
        self.type = type_column
        self.auto_increment = auto_increment
        self.default_value = default_value

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
        if (self.default_value):
            column_sql += f" DEFAULT '{self.default_value}'"

        return column_sql

    def get_dialect(self, dialect: str) -> Dict[str, str]:
        if dialect == 'postgresql':
            return TYPES_SQL_POSTGRES
        elif dialect == 'sqlite':
            return TYPES_SQL_LITE
        else:
            return TYPES_SQL_LITE

    def validate_action(self, on_delete: str, on_update: str):
        valid_on_delete = [member.value for _, member in ActionsEnum.__members__.items() if on_delete.lower() == member.value.lower()]
        if not valid_on_delete:
            raise Exception("ON DELETE with action {on_delete} is invalid".format(on_delete = on_delete))

        valid_on_update = [member.value for _, member in ActionsEnum.__members__.items() if on_update.lower() == member.value.lower()]
        if not valid_on_update:
            raise Exception("ON UPDATE with action {on_update} is invalid.".format(on_update = on_update))



class String(Column, str):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, unique: bool = False,
                 primary_key: bool = False, not_null: bool = False,
                 default_value=None):
        super().__init__(
            'str', unique, primary_key, not_null, default_value=default_value)


class Integer(Column, int):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(
        self, min_value: int = None, unique: bool = False,
        primary_key: bool = False, auto_increment: bool = False,
        not_null: bool = False, default_value=None
    ):
        self.min_value = min_value
        super().__init__(
            'int', unique, primary_key, auto_increment=auto_increment,
            not_null=not_null, default_value=default_value
        )


class BigInteger(Column, int):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, unique: bool = False, primary_key: bool = False,
                 default_value=None):
        super().__init__(
            'bigint', unique, primary_key, default_value=default_value)


class Varchar(Column, str):
    def __new__(cls):
        return super().__new__(cls)

    def __init__(self, length: int, unique: bool = False,
                 primary_key: bool = False, default_value=None):
        self.length = length
        super().__init__(
            'varchar', unique, primary_key, default_value=default_value)

    def column_sql(self, dialect: str):
        column_sql = super().column_sql(dialect)
        return column_sql.format(length=self.length)


class Boolean(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, not_null: bool = False, default_value=None):
        super().__init__(
            'boolean', not_null=not_null, default_value=default_value)
