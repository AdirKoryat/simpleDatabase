from typing import Tuple


from classes.IBaseAction import IBaseAction
from db.db_operations import get_entity_by_key, delete_entity_by_key
from utiles.constants import NONE_STR


class UnsetAction(IBaseAction):

    def __init__(self, variable_name: str) -> None:
        self.variable_name = variable_name

    def execute(self) -> Tuple[str, str]:
        key, old_value = get_entity_by_key(self.variable_name)
        if old_value != NONE_STR:
            delete_entity_by_key(key)

        return key, old_value

    def validate(self):
        pass
