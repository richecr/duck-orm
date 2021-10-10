from typing import Dict
from .model import Model


class ModelManager:
    def __init__(self) -> None:
        self.models: Dict[str, Model] = {}

    def add_model(self, name: str, model: Model):
        self.models[name] = model

    def remove_model(self, name: str):
        del self.models[name]

    async def create_tables(self):
        pass
