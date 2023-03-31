from classes.EndAction import EndAction
from classes.GetAction import GetAction
from classes.IBaseAction import IBaseAction
from classes.NumEqualToAction import NumEqualToAction
from classes.SetAction import SetAction
from classes.UnsetAction import UnsetAction


class WebActionFactory:

    @staticmethod
    def get_action(action_type: str, variable_name: str = None, variable_value: str = None) -> IBaseAction:
        if action_type == 'set':
            return SetAction(variable_name=variable_name, variable_value=variable_value)
        elif action_type == 'get':
            return GetAction(variable_name=variable_name)
        elif action_type == 'unset':
            return UnsetAction(variable_name=variable_name)
        elif action_type == 'numequalto':
            return NumEqualToAction(variable_value=variable_value)
        elif action_type == 'end':
            return EndAction()
        else:
            raise ValueError("No action that match the given type")

