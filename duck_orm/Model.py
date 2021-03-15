from typing import List, Tuple, Type, TypeVar
from databases import Database
import inspect

from duck_orm.sql import fields as fields_type
from duck_orm.utils.functions import get_dialect

T = TypeVar('T', bound='Model')


class Model:
    __tablename__: str = ''
    __db__: Database

    def __init__(self, **kwargs):
        self._instance = {
            'id': None
        }

        for key, value in kwargs.items():
            self._instance[key] = value

        self.type_ = self.__class__

    def __getattribute__(self, key: str):
        _instance = object.__getattribute__(self, '_instance')
        if key in _instance:
            return _instance[key]
        return object.__getattribute__(self, key)

    @classmethod
    def _get_name(cls):
        if cls.__tablename__ == '':
            return cls.__name__.lower()

        return cls.__tablename__

    @classmethod
    def _get_create_sql(cls):
        fields: List[Tuple[str, str]] = []

        for name, field in inspect.getmembers(cls):
            if isinstance(field, fields_type.Column):
                fields.append((name, field.column_sql(cls.__db__.url.dialect)))

        fields_config = [" ".join(field) for field in fields]
        query_executor = get_dialect(str(cls.__db__.url.dialect))
        return query_executor.create_sql(cls._get_name(), fields_config)

    @classmethod
    def _get_select_all_sql(cls, fields: List[str] = []):
        if fields == []:
            fields = ['id']
            for name, field in inspect.getmembers(cls):
                if isinstance(field, fields_type.Column):
                    fields.append(name)

        query_executor = get_dialect(str(cls.__db__.url.dialect))
        sql = query_executor.select_sql(cls._get_name(), fields)
        return sql, fields

    def _get_insert_sql(self):
        fields_name = []
        placeholders = []
        fields_values = {}

        for name, field in inspect.getmembers(self.__class__):
            if isinstance(field, fields_type.Column):
                fields_values[name] = getattr(self, name)
                fields_name.append(name)
                placeholders.append(":{field}".format(field=name))

        query_executor = get_dialect(str(self.__db__.url.dialect))
        sql = query_executor.insert_sql(
            self._get_name(), fields_name, placeholders)
        return sql, fields_values

    @classmethod
    async def create(cls):
        return await cls.__db__.execute(cls._get_create_sql())

    @classmethod
    async def find_all(cls: Type[T], fields: List[str] = []):
        sql, fields = cls._get_select_all_sql(fields)
        data = await cls.__db__.fetch_all(sql)
        result: List[cls] = []
        for row in data:
            entity = dict(zip(fields, row))
            result.append(cls(**entity))

        return result

    @classmethod
    async def find_all_tables(cls):
        query_executor = get_dialect(str(cls.__db__.url.dialect))
        sql = query_executor.select_tables_sql(cls._get_name())
        return await cls.__db__.fetch_all(sql)

    @classmethod
    async def save(cls, model):
        sql, values = model._get_insert_sql()
        cursor = await cls.__db__.execute(query=sql, values=values)
        model._instance['id'] = cursor

    @classmethod
    def _drop_table(cls, name_table: str, dialect: str):
        query_executor = get_dialect(dialect)
        return query_executor.drop_table(name_table)

    @classmethod
    async def drop_table(cls):
        sql = cls._drop_table(cls._get_name(), str(cls.__db__.url.dialect))
        await cls.__db__.execute(sql)
