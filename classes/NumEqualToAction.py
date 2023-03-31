from classes.IBaseAction import IBaseAction
from db.db_operations import get_num_entities_by_value_match


class NumEqualToAction(IBaseAction):

    def __init__(self, variable_value: str) -> None:
        self.variable_value = variable_value

    def execute(self) -> str:
        return str(get_num_entities_by_value_match(self.variable_value))

    def validate(self):
        pass
