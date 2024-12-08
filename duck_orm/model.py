import inspect
from typing import Any, Dict, List, Mapping, Tuple, Type, TypeVar

from databases import Database

from duck_orm.exceptions import IdInvalidException, UpdateException
from duck_orm.sql import fields as fields_type
from duck_orm.sql.condition import Condition
from duck_orm.utils.functions import get_dialect

T = TypeVar("T", bound="Model")


class ModelMeta(type):
    def __new__(cls, name, bases, attrs):
        model_class = super().__new__(cls, name, bases, attrs)

        if "model_manager" in attrs:
            try:
                name = attrs["__tablename__"]
            except KeyError:
                name = name.lower()

            attrs["model_manager"].add_model(name, model_class)

        return model_class


class Model(metaclass=ModelMeta):
    __tablename__: str = ""
    __db__: Database

    def __init__(self, **kwargs):
        self._instance = {}

        for key, value in kwargs.items():
            self._instance[key] = value

    def __getattribute__(self, key: str):
        _instance = object.__getattribute__(self, "_instance")
        result = None
        if key in _instance:
            result = _instance[key]
        else:
            result = object.__getattribute__(self, key)

        from duck_orm.sql.relationship import ManyToMany, OneToMany

        if isinstance(result, (OneToMany, ManyToMany)):
            result.model_ = self
        return result

    def __getitem__(self, key):
        return getattr(self, key)

    @classmethod
    def relationships(cls):
        pass

    @classmethod
    async def associations(cls) -> None:
        cls.relationships()
        sqls: list[str] = []
        dialect = cls.__db__.url.dialect

        for name, field in inspect.getmembers(cls):
            if isinstance(field, fields_type.Column):
                from duck_orm.sql.relationship import ForeignKey, OneToOne

                sql = ""
                if isinstance(field, ForeignKey):
                    field_id = field.model.get_id()[1]
                    sql_field_fk = field_id.type_sql(dialect)
                    sql = field.sql(
                        dialect=dialect,
                        name=name,
                        table_name=cls.get_name(),
                        type_sql=sql_field_fk,
                    )
                elif isinstance(field, OneToOne):
                    if dialect == "sqlite":
                        await cls.drop_table()
                        await cls.create()
                    elif dialect == "postgresql":
                        if not field.model:
                            raise Exception("Model not found")

                        field_id = field.model.get_id()[1]
                        type_sql = field_id.column_sql(dialect)
                        sql = field.sql(
                            dialect=dialect,
                            field_name=name,
                            type_sql=type_sql,
                            table_name=cls.get_name(),
                        )
                if sql != "":
                    sqls.append(sql)

        for sql in sqls:
            await cls.__db__.execute(sql)

    @classmethod
    def get_name(cls):
        return cls.__name__.lower() if cls.__tablename__ == "" else cls.__tablename__

    @classmethod
    def __get_create_sql(cls) -> str:
        fields: List[Tuple[str, str]] = []
        dialect = cls.__db__.url.dialect

        for name, field in inspect.getmembers(cls):
            if isinstance(field, fields_type.Column):
                from duck_orm.sql.relationship import OneToOne

                if isinstance(field, OneToOne):
                    if not field.model:
                        raise Exception("Model not found")

                    field_id = field.model.get_id()[1]
                    table_name = field.model.get_name()
                    fields.extend(
                        (
                            (name, field_id.column_sql(dialect)),
                            ("", field.create_sql(dialect, name, table_name)),
                        )
                    )
                else:
                    fields.insert(0, (name, field.column_sql(dialect)))

        fields_config = [" ".join(field) for field in fields]
        query_executor = get_dialect(str(dialect))
        return query_executor.create_sql(cls.get_name(), fields_config)

    @classmethod
    async def create(cls):
        sql = cls.__get_create_sql()
        return await cls.__db__.execute(sql)

    @classmethod
    def __get_fields_all(cls) -> List[str]:
        cls.relationships()
        fields_all: List[str] = []
        for name, field in inspect.getmembers(cls):
            from duck_orm.sql.relationship import ManyToMany, OneToMany

            if isinstance(field, fields_type.Column) and not isinstance(field, (OneToMany, ManyToMany)):
                fields_all.append(name)
        return fields_all

    @classmethod
    def get_id(cls):
        for name, field in inspect.getmembers(cls):
            if isinstance(field, fields_type.Column) and field.primary_key:
                return name, field
        raise IdInvalidException("Model has no primary key!")

    @classmethod
    def __get_select_sql(
        cls,
        fields_includes: List[str] = [],
        fields_excludes: List[str] = [],
        conditions: List[Condition] = [],
        limit: int | None = None,
    ) -> tuple[str, list[str]]:
        if not fields_includes:
            fields_includes = cls.__get_fields_all()
        fields_includes = list(set(fields_includes) - set(fields_excludes))

        query_executor = get_dialect(str(cls.__db__.url.dialect))
        conditions_str = "1 = 1"
        if conditions:
            conditions_str = " and ".join(map(lambda condition: condition.get_condition(), conditions))

        sql = query_executor.select_sql(cls.get_name(), fields_includes, conditions_str, limit)
        return sql, fields_includes

    @classmethod
    async def __parser_fields(cls, data: Mapping):
        fields_all: List[Tuple[str, fields_type.Column | fields_type.Timestamp] | str] = []
        from duck_orm.sql.relationship import ForeignKey, ManyToOne, OneToMany, OneToOne

        fields_foreign_key: Dict[str, OneToMany] = {}
        for name, field in inspect.getmembers(cls):
            if isinstance(field, fields_type.Column):
                if isinstance(field, fields_type.Timestamp):
                    fields_all.append((name, field))
                else:
                    fields_all.append(name)

                if isinstance(field, (ManyToOne, OneToOne, ForeignKey)):
                    if not field.model:
                        raise Exception("Model not found")

                    field_name = field.model.get_id()[0]
                    condition_with_id = Condition(field_name, "=", data[name])
                    model_entity = await field.model.find_one(conditions=[condition_with_id])
                    fields_foreign_key[name] = model_entity
                elif isinstance(field, OneToMany):
                    fields_foreign_key[name] = field

        return fields_all, fields_foreign_key

    @classmethod
    async def find_all(
        cls: Type[T],
        fields_includes: List[str] = [],
        fields_excludes: List[str] = [],
        conditions: List[Condition] = [],
        limit: int | None = None,
    ):
        sql, fields_includes = cls.__get_select_sql(fields_includes, fields_excludes, conditions, limit=limit)
        data = await cls.__db__.fetch_all(sql)
        result: List[T] = []
        dialect = get_dialect(str(cls.__db__.url.dialect))
        for row in data:
            row_ = row._mapping
            fields_all, fields_foreign_key = await cls.__parser_fields(row_)
            entity = dialect.parser(row_, fields_all, fields_foreign_key)
            result.append(cls(**entity))

        return result

    @classmethod
    async def find_one(
        cls: Type[T],
        fields_includes: List[str] = [],
        fields_excludes: List[str] = [],
        conditions: List[Condition] = [],
    ):
        sql, fields_includes = cls.__get_select_sql(fields_includes, fields_excludes, conditions, limit=1)
        data = await cls.__db__.fetch_one(sql)
        dialect = get_dialect(str(cls.__db__.url.dialect))
        result: T | None = None
        if data is not None:
            data_dict = data._mapping
            fields_all, fields_foreign_key = await cls.__parser_fields(data_dict)
            entity = dialect.parser(data_dict, fields_all, fields_foreign_key)
            result = cls(**entity)
        return result

    @classmethod
    async def find_by_id(
        cls: Type[T],
        id: Any,
        fields_includes: List[str] = [],
        fields_excludes: List[str] = [],
    ):
        name = cls.get_id()[0]
        condition = Condition(name, "=", id)
        return await cls.find_one(
            fields_includes=fields_includes,
            fields_excludes=fields_excludes,
            conditions=[condition],
        )

    @classmethod
    async def find_all_tables(cls) -> List[dict]:
        query_executor = get_dialect(str(cls.__db__.url.dialect))
        sql = query_executor.select_tables_sql()
        data = await cls.__db__.fetch_all(sql)
        result: List[dict] = []
        for row in data:
            entity = query_executor.parser(row._mapping, [("name")])
            result.append(entity)
        return result

    def __get_insert_sql(self):
        fields_name = []
        placeholders = []
        fields_values = {}

        for name, field in self._instance.items():
            value = self[name]
            if isinstance(field, Model):
                name_id_fk = field.get_id()[0]
                value = self[name][name_id_fk]

            fields_values[name] = value
            fields_name.append(name)
            placeholders.append(":{field}".format(field=name))

        query_executor = get_dialect(str(self.__db__.url.dialect))
        sql = query_executor.insert_sql(self.get_name(), fields_name, placeholders)
        return sql, fields_values

    @classmethod
    def __get_sql_last_inserted_id(cls):
        name, _ = cls.get_id()
        query_executor = get_dialect(str(cls.__db__.url.dialect))
        return query_executor.select_last_id(name, cls.get_name())

    async def __get_last_insert_id(self):
        sql = self.__get_sql_last_inserted_id()
        return await self.__db__.fetch_one(sql)

    @classmethod
    async def save(cls, model: T):
        sql, values = model.__get_insert_sql()
        await cls.__db__.execute(query=sql, values=values)
        data = await model.__get_last_insert_id()
        name, field = cls.get_id()
        if data is not None:
            data = data._mapping
            from duck_orm.sql.relationship import OneToOne

            if isinstance(field, OneToOne):
                field_model = model._instance[name]
                if isinstance(field_model, Model):
                    name_id_model = field_model.get_id()[0]
                    field_model.__setattr__(name_id_model, data[name])
                    model._instance[name] = field_model
            else:
                model._instance[name] = data[name]
        return model

    def __update_sql(self, fields: List[str]):
        field_name_id = self.get_id()[0]
        field_id = self[field_name_id]

        if field_id is None:
            raise UpdateException(f"Updating by ID requires that the object {self} has an ID field")

        condition = [f"{field_name_id} = {field_id}"]
        query_executor = get_dialect(str(self.__db__.url.dialect))
        sql = query_executor.update_sql(self.get_name(), fields, conditions=condition)

        return sql, field_name_id, field_id

    async def update(self, **kwargs):
        fields = []
        values = {}
        for name, value in kwargs.items():
            if isinstance(value, Model):
                name_id_fk = value.get_id()[0]
                value = value[name_id_fk]

            fields_tmp = "{field} = :{field}".format(field=name)
            fields.append(fields_tmp)
            values[name] = value

        sql, field_name_id, field_id = self.__update_sql(fields)
        await self.__db__.execute(query=sql, values=values)
        condition_with_id = Condition(field_name_id, "=", field_id)
        return await self.find_one(conditions=[condition_with_id])

    @classmethod
    def __drop_table(cls, dialect: str, name_table: str, cascade: bool = False):
        query_executor = get_dialect(dialect)
        return query_executor.drop_table(name_table, cascade)

    @classmethod
    async def drop_table(cls, cascade: bool = False):
        sql = cls.__drop_table(str(cls.__db__.url.dialect), cls.get_name(), cascade)
        await cls.__db__.execute(sql)

    @classmethod
    def __delete(cls, name_table: str, conditions: List[Condition], dialect: str) -> str:
        query_executor = get_dialect(dialect)
        conditions_str = " and ".join(map(lambda condition: condition.get_condition(), conditions))
        return query_executor.delete_sql(name_table, conditions_str)

    @classmethod
    async def delete(cls, conditions: List[Condition]):
        try:
            dialect = cls.__db__.url.dialect
            sql = cls.__delete(cls.get_name(), conditions, str(dialect))
            await cls.__db__.execute(sql)
        except Exception as ex:
            Exception("DELETE ERROR: {ex}".format(ex=ex))
