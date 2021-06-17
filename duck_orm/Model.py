import inspect
from databases import Database
from typing import Dict, List, Tuple, Type, TypeVar, Union

from duck_orm.sql.Condition import Condition
from duck_orm.sql import fields as fields_type
from duck_orm.utils.functions import get_dialect
from duck_orm.Exceptions.UpdateException import UpdateException

T = TypeVar('T', bound='Model')


class Model:
    __tablename__: str = ''
    __db__: Database

    def __init__(self, **kwargs):
        self._instance = {}

        for key, value in kwargs.items():
            self._instance[key] = value

        for name, field in inspect.getmembers(self.__class__):
            from duck_orm.sql.relationship import OneToMany
            if isinstance(field, OneToMany):
                field.model_ = self

    def __getattribute__(self, key: str):
        _instance = object.__getattribute__(self, '_instance')
        if key in _instance:
            return _instance[key]
        return object.__getattribute__(self, key)

    def __getitem__(self, key):
        return getattr(self, key)

    @classmethod
    def relationships(cls):
        pass

    @classmethod
    async def associations(cls):
        cls.relationships()
        sqls: list[str] = []
        for name, field in inspect.getmembers(cls):
            if isinstance(field, fields_type.Column):
                from duck_orm.sql.relationship import OneToMany, OneToOne
                if (isinstance(field, OneToMany)):
                    sql = field.sql().format(name=field.name_in_person,
                                             name_table=cls.get_name(), field_name=cls.get_id()[0])
                    sqls.append(sql)

                elif isinstance(field, OneToOne):
                    name_relationship, _ = field.model.get_id()
                    sql = field.sql().format(table=cls.get_name(),
                                             name_table=field.model.get_name(), field_name=name_relationship)
                    sqls.append(sql)

        for sql in sqls:
            await cls.__db__.execute(sql)

    @ classmethod
    def get_name(cls):
        if cls.__tablename__ == '':
            return cls.__name__.lower()

        return cls.__tablename__

    @ classmethod
    def __get_create_sql(cls):
        fields: List[Tuple[str, str]] = []

        for name, field in inspect.getmembers(cls):
            if isinstance(field, fields_type.Column):
                from duck_orm.sql.relationship import OneToMany, ManyToOne, OneToOne
                if (isinstance(field, ManyToOne)):
                    field_relationship = field.model.get_id()[1]
                    fields.append(
                        (name, field_relationship.type_sql(cls.__db__.url.dialect)))
                elif (isinstance(field, OneToMany)):
                    name_relationship, field_relationship = field.model.get_id()
                    fields.append(
                        (name, field_relationship.type_sql(cls.__db__.url.dialect)))
                    fields.append(('', field.sql().format(
                        name=name, name_table=field.model.get_name(), field_name=name_relationship)))
                elif (isinstance(field, OneToOne)):
                    name_relationship, field_relationship = field.model.get_id()
                    fields.append(
                        (name, field_relationship.column_sql(cls.__db__.url.dialect)))
                    fields.append(('', field.sql().format(
                        name=name, name_table=field.model.get_name(), field_name=name_relationship)))
                else:
                    fields.insert(0,
                                  (name, field.column_sql(cls.__db__.url.dialect)))

        fields_config = [" ".join(field) for field in fields]
        query_executor = get_dialect(str(cls.__db__.url.dialect))
        return query_executor.create_sql(cls.get_name(), fields_config)

    @ classmethod
    async def create(cls):
        sql = cls.__get_create_sql()
        return await cls.__db__.execute(sql)

    @ classmethod
    def __get_fields_all(cls) -> List[str]:
        fields_all: List[str] = []
        for name, field in inspect.getmembers(cls):
            from duck_orm.sql.relationship import OneToMany
            if isinstance(field, fields_type.Column) and not isinstance(field, OneToMany):
                fields_all.append(name)

        return fields_all

    @ classmethod
    def get_id(cls):
        for name, field in inspect.getmembers(cls):
            if isinstance(field, fields_type.Column):
                if (field.primary_key):
                    return name, field

        raise Exception('Model não tem chave primária')

    @ classmethod
    def __get_select_sql(cls, fields_includes: List[str] = [], fields_excludes: List[str] = [], conditions: List[Condition] = [], limit: int = None):
        if fields_includes == []:
            fields_includes = cls.__get_fields_all()
        fields_includes = list(set(fields_includes) - set(fields_excludes))

        query_executor = get_dialect(str(cls.__db__.url.dialect))
        conditions_str = '1 = 1'
        if len(conditions) > 0:
            conditions_str = ' and '.join(
                map(lambda condition: condition.get_condition(), conditions))

        sql = query_executor.select_sql(
            cls.get_name(), fields_includes, conditions_str, limit)
        return sql, fields_includes

    @ classmethod
    async def find_all(cls: Type[T], fields_includes: List[str] = [], fields_excludes: List[str] = [], conditions: List[Condition] = [], limit: int = None):
        sql, fields_includes = cls.__get_select_sql(
            fields_includes, fields_excludes, conditions, limit=limit)
        data = await cls.__db__.fetch_all(sql)
        result: List[cls] = []
        dialect = get_dialect(str(cls.__db__.url.dialect))
        for row in data:
            row = dict(row.items())
            fields_all: List[str] = []
            fields_foreign_key: Dict[str, OneToMany] = {}
            for name, field in inspect.getmembers(cls):
                if isinstance(field, fields_type.Column):
                    fields_all.append(name)
                    from duck_orm.sql.relationship import OneToMany, ManyToOne
                    if isinstance(field, ManyToOne):
                        field_id = field.model.get_id()[0]
                        model_entity = await field.model.find_one(conditions=[
                            Condition(field_id, '=', row[name])
                        ])
                        fields_foreign_key[name] = model_entity

            entity = dialect.parser(row, fields_all, fields_foreign_key)
            result.append(cls(**entity))

        return result

    @ classmethod
    async def find_one(cls: Type[T],  fields_includes: List[str] = [], fields_excludes: List[str] = [], conditions: List[Condition] = []):
        sql, fields_includes = cls.__get_select_sql(
            fields_includes, fields_excludes, conditions, limit=1)
        data = await cls.__db__.fetch_one(sql)
        dialect = get_dialect(str(cls.__db__.url.dialect))
        entity = None
        result: cls = None
        if (data != None):
            data = dict(data.items())
            entity = dialect.parser(data, cls.__get_fields_all())
            result: cls = cls(**entity)
        return result

    @ classmethod
    async def find_all_tables(cls):
        query_executor = get_dialect(str(cls.__db__.url.dialect))
        sql = query_executor.select_tables_sql(cls.get_name())
        data = await cls.__db__.fetch_all(sql)
        result: List = []
        for row in data:
            row = dict(row.items())
            entity = query_executor.parser(row)
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
        sql = query_executor.insert_sql(
            self.get_name(), fields_name, placeholders)
        return sql, fields_values

    @classmethod
    def __get_sql_last_inserted_id(cls):
        name, _ = cls.get_id()
        query_executor = get_dialect(str(cls.__db__.url.dialect))
        sql = query_executor.select_last_id(name, cls.get_name())
        return sql

    async def __get_last_insert_id(self):
        sql = self.__get_sql_last_inserted_id()
        return await self.__db__.fetch_one(sql)

    @ classmethod
    async def save(cls, model: T):
        sql, values = model.__get_insert_sql()
        await cls.__db__.execute(query=sql, values=values)
        data = await model.__get_last_insert_id()
        name, _ = cls.get_id()
        if (data != None):
            data = dict(data.items())
            model._instance[name] = data[name]
        return model

    def __update_sql(self, fields: List[str]):
        field_id: Union[Tuple[str, fields_type.Column], None] = None
        for name, field in inspect.getmembers(self.__class__):
            if isinstance(field, fields_type.Column):
                if field.primary_key and field.auto_increment:
                    field_id = name, self.__getattribute__(name)

        if (field_id[1] == None):
            raise UpdateException(
                "Updating by ID requires that the object {self} has an ID field".format(self=self))

        condition = ['{field} = {value}'.format(
            field=field_id[0], value=field_id[1])]
        query_executor = get_dialect(str(self.__db__.url.dialect))
        sql = query_executor.update_sql(
            self.get_name(), fields, conditions=condition)

        return sql, field_id

    async def update(self, **kwargs):
        fields = []
        values = {}
        for name, value in kwargs.items():
            fields_tmp = "{field} = :{field_bind_value}".format(
                field=name, field_bind_value=name)
            fields.append(fields_tmp)
            values[name] = value

        sql, field_id = self.__update_sql(fields)
        await self.__db__.execute(query=sql, values=values)
        return await self.find_one(conditions=[
            Condition(field_id[0], '=', field_id[1])
        ])

    @ classmethod
    def __drop_table(cls, name_table: str, dialect: str):
        query_executor = get_dialect(dialect)
        return query_executor.drop_table(name_table)

    @ classmethod
    async def drop_table(cls):
        sql = cls.__drop_table(cls.get_name(), str(cls.__db__.url.dialect))
        await cls.__db__.execute(sql)

    @ classmethod
    def __delete(cls, name_table: str, conditions: List[Condition], dialect: str):
        query_executor = get_dialect(dialect)
        conditions_str = ' and '.join(
            map(lambda condition: condition.get_condition(), conditions))
        return query_executor.delete_sql(name_table, conditions_str)

    @ classmethod
    async def delete(cls, conditions: List[Condition]):
        try:
            sql = cls.__delete(cls.get_name(), conditions,
                               str(cls.__db__.url.dialect))
            await cls.__db__.execute(sql)
        except Exception as ex:
            print('DELETE ERROR: {ex}'.format(ex=ex))
