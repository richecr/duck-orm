from duck_orm.sql.Condition import Condition
from typing import Type

from duck_orm.Model import Model
from duck_orm.sql.fields import Column


class OneToMany(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, model: Type[Model], name_in_person: str, name_relation: str):
        self.model = model
        self.name_in_person = name_in_person
        self.model_: Type[Model] = None
        if not name_relation:
            raise Exception('Attribute name_relation is mandatory')
        self.name_relation = name_relation
        super().__init__('OneToMany')

    async def add(self, model: Type[Model]):
        model._instance[self.name_in_person] = self.model_
        return await self.model.save(model)

    async def get_all(self):
        return await self.model.find_all(conditions=[
            Condition(self.name_in_person, '=',
                      self.model_[self.model_.get_id()[0]])
        ])

    def sql_column(self, type_sql: str):
        sql = 'ALTER TABLE ' + self.model.get_name() + \
            ' ADD {name} ' + type_sql
        return sql

    def sql(self):
        column_sql = 'ALTER TABLE ' + self.model.get_name() + \
            ' ADD CONSTRAINT ' + self.name_relation + \
            ' FOREIGN KEY ({name}) REFERENCES {name_table} ({field_name})'
        return column_sql


class ManyToOne(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, model: Type[Model]):
        self.model = model
        super().__init__('OneToMany')


class OneToOne(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, model: Type[Model]):
        self.model = model
        super().__init__('OneToOne', primary_key=True)

    def sql(self):
        column_sql = 'FOREIGN KEY ({name}) REFERENCES {name_table} ({field_name})'
        return column_sql
