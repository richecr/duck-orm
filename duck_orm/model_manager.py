import logging
from typing import Dict, List
from databases.core import Database

from duck_orm.model import Model
from duck_orm.sql import fields as fields_type
from duck_orm.utils.functions import get_dialect


class ModelManager:
    def __init__(self) -> None:
        self.models: Dict[str, Model] = {}
        self.db_connection: Database = None

    def add_model(self, name: str, model: Model):
        self.models[name] = model

    def remove_model(self, name: str):
        del self.models[name]

    def __get_table_name(self, table_obj: dict[str, str]) -> str:
        try:
            return table_obj["name"]
        except KeyError:
            return table_obj["tablename"]

    async def create_all_tables(self, models_db: List = None):
        if models_db is None:
            models_db = []
        logging.info("Starts creating all tables in the database.")
        if len(self.models) > 0:
            for name, model in self.models.items():
                logging.info(f"Create table {name}!")
                await model.create()

            logging.info("Creation of table associations in the database.")
            models_db = list(map(lambda model: self.__get_table_name(model), models_db))
            for name, model in self.models.items():
                if name not in models_db:
                    await model.associations()
                else:
                    model.relationships()
        else:
            logging.error("No models found")
            Exception(
                "No models found: I created your models and put the "
                + "model_manager attribute on them."
            )

    async def drop_all_tables(self):
        logging.info("Delete all tables in the database.")
        for _, model in self.models.items():
            await model.drop_table(cascade=True)

    def get_database(self):
        from importlib.machinery import SourceFileLoader

        file = SourceFileLoader("module.name", "./duckorm_file.py").load_module()
        dialect = file.configs["development"]["client"]
        database_url = file.configs["development"]["database_url"]
        url = "{}:///{}" if dialect == "sqlite3" else "{}://{}"
        db = Database(url.format(dialect, database_url))
        self.db_connection = db

    async def create_table(self, name_table, fields):
        self.get_database()
        sqls: list[str] = []
        dialect = self.db_connection.url.dialect

        for name, field in fields.items():
            if isinstance(field, fields_type.Column):
                from duck_orm.sql.relationship import ForeignKey, OneToOne

                sql = ""
                if isinstance(field, OneToOne):
                    sql = f"{name} {field.type_fk.type_sql(dialect=dialect)}, "
                    sql += field.sql_migration(dialect, name)
                elif isinstance(field, ForeignKey):
                    field_id = field.model.get_id()[1]
                    sql_field_fk = field_id.type_sql(dialect)
                    sql = field.sql(
                        dialect=dialect,
                        name=name,
                        table_name=name,
                        type_sql=sql_field_fk,
                    )
                else:
                    sql = f"{name} {field.column_sql(dialect)}"

                if sql != "":
                    sqls.append(sql)

        query_executor = get_dialect(str(dialect))
        sql_ = query_executor.create_sql(name_table, sqls)
        logging.info(f"MIGRATION -> SQL Executed: {sql}")
        await self._execute_sql(sql_)

    async def drop_table(self, name):
        self.get_database()
        dialect = self.db_connection.url.dialect
        query_executor = get_dialect(dialect)
        sql_drop = query_executor.drop_table(name, True)
        await self._execute_sql(sql_drop)

    async def _execute_sql(self, sql: str):
        await self.db_connection.connect()
        await self.db_connection.execute(sql)
        await self.db_connection.disconnect()
