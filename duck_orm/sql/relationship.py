from typing import Type

from duck_orm.Model import Model
from duck_orm.sql.fields import Column


class OneToMany(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, model: Type[Model]):
        self.model = model
        super().__init__('OneToMany')

    def sql(self):
        column_sql = 'FOREIGN KEY ({name}) REFERENCES {name_table} ({field_name})'
        return column_sql


class OneToOne(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, model: Type[Model]):
        self.model = model
        super().__init__('OneToMany', primary_key=True)

    def sql(self):
        column_sql = 'FOREIGN KEY ({name}) REFERENCES {name_table} ({field_name})'
        return column_sql
