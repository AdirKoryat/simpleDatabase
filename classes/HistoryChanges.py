import logging
from collections import deque


from db.db_operations import  delete_entity_by_key, store_variable
from utiles.constants import  NONE_STR, NO_COMMANDS_STR

undo_stack = deque()
redo_stack = deque()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class HistoryChanges:

    @staticmethod
    def push(key: str, old_value: str) -> None:
        undo_stack.append((key, old_value))
        logger.info(f'undo stack state: {undo_stack}')

    @staticmethod
    def undo() -> str:
        output = NO_COMMANDS_STR
        if undo_stack:
            variable_name, variable_value = undo_stack.pop()
            variable_name, old_value = store_variable(variable_name, variable_value)
            redo_stack.append((variable_name, old_value))
            logger.info(f'UNDO: redo stack state: {redo_stack}')
            if variable_value == NONE_STR:
                delete_entity_by_key(variable_name)

            output = f'{variable_name} = {variable_value}'
            logger.info(f'UNDO: undo stack state: {undo_stack}')
        return output

    @staticmethod
    def redo() -> str:
        output = NO_COMMANDS_STR
        if redo_stack:
            variable_name, variable_value = redo_stack.pop()
            if variable_value == NONE_STR:
                delete_entity_by_key(variable_name)
            else:
                store_variable(variable_name, variable_value)

            output = f'{variable_name} = {variable_value}'
            logger.info(f'REDO: redo stack state: {redo_stack}')

        return output

    @staticmethod
    def clear() -> None:
        undo_stack.clear()
        redo_stack.clear()
        logger.info(f'Empty stacks...\n undo = {undo_stack}\n redo = {redo_stack}')
