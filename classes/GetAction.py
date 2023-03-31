from classes.IBaseAction import IBaseAction
from db.db_operations import get_entity_by_key


class GetAction(IBaseAction):

    def __init__(self, variable_name: str) -> None:
        self.variable_name = variable_name

    def execute(self) -> str:
        key, value = get_entity_by_key(self.variable_name)

        return f'{key} = {value}'

    def validate(self):
        pass
