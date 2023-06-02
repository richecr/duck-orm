import inspect
from typing import Any, Dict, List, Optional, Type, Union

from duck_orm.model import Model
from duck_orm.sql.condition import Condition
from duck_orm.utils.functions import get_dialect
from duck_orm.sql.fields import Column, ActionsEnum


class ForeignKey(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(
        self,
        model: Type[Model],
        name_in_table_fk: str,
        unique: bool = False,
        name_constraint: str = "",
        on_delete: ActionsEnum = ActionsEnum.NO_ACTION,
        on_update: ActionsEnum = ActionsEnum.CASCADE,
    ) -> None:
        self.validate_action(on_delete.value, on_update.value)
        self.model = model
        self.name_in_table_fk = name_in_table_fk
        self.unique = unique
        self.on_delete = on_delete.value
        self.on_update = on_update.value
        self.name_constraint = name_constraint
        super().__init__("ForeignKey", unique=unique)

    def sql(self, dialect: str, name: str, table_name: str, type_sql: str) -> str:
        generator_sql = get_dialect(dialect)
        args = {
            "field_name": name,
            "field_type": type_sql,
            "table_name": table_name,
            "on_delete": self.on_delete,
            "on_update": self.on_update,
            "field": self.name_in_table_fk,
            "table_relation": self.model.get_name(),
            "name_constraint": self.name_constraint,
        }
        return generator_sql.alter_table_add_column_with_constraint(**args)


class OneToMany(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, model: Type[Model], name_in_table_fk: str) -> None:
        self.model = model
        self.name_in_table_fk = name_in_table_fk
        self.model_: Union[Type[Model], None] = None
        super().__init__("OneToMany")

    async def add(self, model: Type[Model]):
        if self.model_:
            model._instance[self.name_in_table_fk] = self.model_
        self.model_ = None
        return await self.model.save(model)

    async def get_all(self):
        result: List[Model] = []
        if not self.model_:
            return await self.model.find_all()
        field_name = self.model_.get_id()[0]
        condition = Condition(self.name_in_table_fk, "=", self.model_[field_name])
        return await self.model.find_all(conditions=[condition])


class ManyToOne(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, model: Type[Model]):
        self.model = model
        super().__init__("OneToMany")


class OneToOne(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(
        self,
        model: Type[Model] = None,
        name_constraint: str = "",
        on_delete: ActionsEnum = ActionsEnum.NO_ACTION,
        on_update: ActionsEnum = ActionsEnum.CASCADE,
        name_model: str = "",
        name_fk: str = "",
        type_fk: Column = None,
    ) -> None:
        self.validate_action(on_delete.value, on_update.value)
        self.model = model
        self.name_constraint = name_constraint
        self.on_delete = on_delete.value
        self.on_update = on_update.value
        self.name_model = name_model
        self.name_fk = name_fk
        self.type_fk = type_fk
        super().__init__("OneToOne", primary_key=True)

    def create_sql(self, dialect: str, field_name: str, name_table: str):
        generator_sql = get_dialect(dialect)
        field = self.model.get_id()[0]
        return generator_sql.add_foreing_key_column(
            field=field,
            name=field_name,
            table_name=name_table,
            on_delete=self.on_delete,
            on_update=self.on_update,
            name_constraint=self.name_constraint,
        )

    def sql(
        self, dialect: str, field_name: str, type_sql: str, table_name: str = ""
    ) -> str:
        generator_sql = get_dialect(dialect)
        field = self.model.get_id()[0]
        sql = ""
        return (
            generator_sql.alter_table_add_column_with_constraint(
                table_name=table_name,
                field_name=field_name,
                field_type=type_sql,
                field=field,
                table_relation=self.model.get_name(),
                name_constraint=self.name_constraint,
                on_delete=self.on_delete,
                on_update=self.on_update,
            )
            if table_name != ""
            else generator_sql.add_foreing_key_column(
                name=field_name,
                table_name=table_name,
                field=field,
                on_delete=self.on_delete,
                on_update=self.on_update,
                name_constraint=self.name_constraint,
            )
        )

    def sql_migration(self, dialect: str, field_name: str) -> str:
        generator_sql = get_dialect(dialect)
        return generator_sql.add_foreing_key_column(
            name=field_name,
            table_name=self.name_model,
            field=self.name_fk,
            on_delete=self.on_delete,
            on_update=self.on_update,
            name_constraint=self.name_constraint,
        )


class ManyToMany(Column):
    def __new__(cls, **kwargs):
        return super().__new__(cls)

    def __init__(self, model: Type[Model], model_relation: Type[Model]):
        self.model = model
        self.model_: Type[Model] = None
        self.model_relation = model_relation
        super().__init__("ManyToMany")

    async def add_models(self, model_instance_one: Model, model_instance_two: Model):
        model_dict: Dict[str, Any] = {}
        for name, field in inspect.getmembers(self.model_relation):
            if (isinstance(field, ForeignKey)) and not field.primary_key:
                if isinstance(model_instance_one, field.model):
                    name_field = model_instance_one.get_id()[0]
                    model_dict[name] = model_instance_one[name_field]
                elif isinstance(model_instance_two, field.model):
                    name_field = model_instance_two.get_id()[0]
                    model_dict[name] = model_instance_two[name_field]

        model_save = self.model_relation(**model_dict)
        self.model_ = None
        return await self.model_relation.save(model_save)

    async def add(self, model_instance_one: Model):
        model_dict: Dict[str, Any] = {}
        for name, field in inspect.getmembers(self.model_relation):
            if (isinstance(field, ForeignKey)) and not field.primary_key:
                if isinstance(model_instance_one, field.model):
                    name_field = model_instance_one.get_id()[0]
                    model_dict[name] = model_instance_one[name_field]
                elif isinstance(self.model_, field.model):
                    name_field = self.model_.get_id()[0]
                    model_dict[name] = self.model_[name_field]

        model_save = self.model_relation(**model_dict)
        self.model_ = None
        return await self.model_relation.save(model_save)

    async def get_all(self):
        if self.model_:
            field_name = self.model_.get_id()[0]
            value_field = self.model_[field_name]
            field_name_relation = ""

        field_name_other_model = ""
        for name, field in inspect.getmembers(self.model_relation):
            if (isinstance(field, ForeignKey)) and not field.primary_key:
                if self.model == field.model:
                    field_name_other_model = name
                elif isinstance(self.model_, field.model):
                    field_name_relation = name

        models_relations: List[Model] = []
        if self.model_:
            condition = Condition(field_name_relation, "=", value_field)
            models_relations = await self.model_relation.find_all(
                conditions=[condition]
            )
        else:
            models_relations = await self.model_relation.find_all()

        return list(map(lambda model: model[field_name_other_model], models_relations))
