from google.cloud import datastore

datastore_client = datastore.Client()
KIND = 'variable'


def store_variable(variable_name: str, variable_value: str) -> None:
    complete_key = datastore_client.key(KIND, variable_name)
    entity = datastore.Entity(key=complete_key)

    entity.update(
        {
            'value': variable_value
        }
    )
    datastore_client.put(entity)


def get_variable_value(variable_name: str) -> str:
    key = datastore_client.key(KIND, variable_name)
    entity = datastore_client.get(key)
    if entity:
        return entity['value']

    return 'None'


def delete_all_entities() -> None:
    entities = list(datastore_client.query(kind='variable').fetch())
    datastore_client.delete_multi([entity.key for entity in entities])
