import logging

from typing import Dict, List
from duck_orm.model import Model


class ModelManager:
    def __init__(self) -> None:
        self.models: Dict[str, Model] = {}

    def add_model(self, name: str, model: Model):
        self.models[name] = model

    def remove_model(self, name: str):
        del self.models[name]

    def __get_table_name(self, table_obj: dict[str, str]) -> str:
        try:
            return table_obj['name']
        except KeyError:
            return table_obj['tablename']

    async def create_all_tables(self, models_db: List = []):
        logging.info("Starts creating all tables in the database.")
        if len(self.models) > 0:
            for name, model in self.models.items():
                logging.info("Create table {}!".format(name))
                await model.create()

            logging.info("Creation of table associations in the database.")
            models_db = list(
                map(lambda model: self.__get_table_name(model), models_db))
            for name, model in self.models.items():
                if name not in models_db:
                    await model.associations()
                else:
                    model.relationships()
        else:
            logging.error("No models found")
            Exception(
                "No models found: I created your models and put the " +
                "model_manager attribute on them.")

    async def drop_all_tables(self):
        logging.info("Delete all tables in the database.")
        for _, model in self.models.items():
            await model.drop_table(cascade=True)
