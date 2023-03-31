import logging
from typing import Tuple

from google.cloud import datastore

from utiles.constants import KIND, NONE_STR, VALUE_ATTRIBUTE

datastore_client = datastore.Client()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def store_variable(variable_name: str, variable_value: str) -> Tuple[str, str]:
    """
    Insert new entity in case that the given key is not exists
    otherwise Update this entity.
    In case of `variable_value` in 'None' we don't store it.
    :param variable_name: The key entity.
    :param variable_value: The value of this entity.
    :return: Tuple of previous key and value if exists otherwise return the key with value 'None'.
    """
    complete_key = datastore_client.key(KIND, variable_name)
    key, old_value = get_entity_by_key(variable_name)

    if variable_value == NONE_STR:
        return variable_name, old_value

    entity = datastore.Entity(key=complete_key)

    entity.update(
        {
            'value': variable_value
        }
    )
    logger.info(f'save entity: {entity}')
    datastore_client.put(entity)

    return variable_name, old_value


def get_entity_by_key(key: str) -> Tuple[str, str]:
    """
    :param key: Entity key.
    :return:  Return key and value of the entity.

    """
    complete_key = datastore_client.key(KIND, key)
    entity = datastore_client.get(complete_key)
    value = NONE_STR
    if entity:
        value = entity[VALUE_ATTRIBUTE]
    logger.info(f'get entity by key return: {entity}')
    return key, value


def get_num_entities_by_value_match(value: str) -> int:
    """
    :param value: Filter value.
    :return: number of entities that match the given value.
             Return 0 if there is no match.
    """
    query = datastore_client.query(kind=KIND)
    return len(list(query.add_filter('value', '=', value).fetch()))


def delete_entity_by_key(key: str) -> None:
    complete_key = datastore_client.key(KIND, key)
    datastore_client.delete(complete_key)


def delete_all_entities() -> None:
    entities = list(datastore_client.query(kind=KIND).fetch())
    datastore_client.delete_multi([entity.key for entity in entities])
