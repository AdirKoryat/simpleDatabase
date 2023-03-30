from google.cloud import datastore
from google.cloud.datastore import Entity

from utiles.constants import KIND

datastore_client = datastore.Client()


def store_variable(variable_name: str, variable_value: str) -> None:
    """
    Insert new entity in case that the given key is not exists
    otherwise Update this entity.
    :param variable_name: The key entity.
    :param variable_value: The value of this entity.
    :return: None.
    """
    complete_key = datastore_client.key(KIND, variable_name)
    entity = datastore.Entity(key=complete_key)

    entity.update(
        {
            'value': variable_value
        }
    )
    datastore_client.put(entity)


def get_entity_by_key(key: str) -> Entity:
    """
    :param key: entity key.
    :return:  return datastore Entity and None if empty.
    """
    complete_key = datastore_client.key(KIND, key)
    return datastore_client.get(complete_key)


def get_entities_by_value(value: str) -> list:
    """
    :param value: Filter value.
    :return: List of all entities that match the given value.
             Return empty list if there is no match.
    """
    query = datastore_client.query(kind=KIND)
    return list(query.add_filter('value', '=', value).fetch())


def delete_entity_by_key(key: str) -> None:
    complete_key = datastore_client.key(KIND, key)
    datastore_client.delete(complete_key)


def delete_all_entities() -> None:
    entities = list(datastore_client.query(kind=KIND).fetch())
    datastore_client.delete_multi([entity.key for entity in entities])
