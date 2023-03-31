from typing import Tuple


from classes.IBaseAction import IBaseAction
from db.db_operations import store_variable
from utiles.validations import validate_input


class SetAction(IBaseAction):

    def __init__(self, variable_name: str, variable_value: str) -> None:
        self.variable_name = variable_name
        self.variable_value = variable_value

    def execute(self) -> Tuple[str, str]:
        return store_variable(self.variable_name, self.variable_value)

    def validate(self) -> None:
        if not validate_input(self.variable_name) or not validate_input(self.variable_value):
            raise ValueError("name and value variables must not be empty and not contain any spaces.")
