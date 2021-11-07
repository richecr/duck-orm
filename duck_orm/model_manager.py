from typing import Dict, List
from .model import Model


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
        if len(self.models) > 0:
            for _, model in self.models.items():
                await model.create()

            models_db = list(
                map(lambda model: self.__get_table_name(model), models_db))
            for name, model in self.models.items():
                if name not in models_db:
                    await model.associations()
                else:
                    model.relationships()
        else:
            Exception(
                "No models found: I created your models and put the " +
                "model_manager attribute on them.")

    async def drop_all_tables(self):
        for _, model in self.models.items():
            await model.drop_table(cascade=True)
