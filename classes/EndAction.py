from classes.IBaseAction import IBaseAction
from db.db_operations import delete_all_entities


class EndAction(IBaseAction):

    def execute(self) -> None:
        delete_all_entities()

    def validate(self):
        pass
