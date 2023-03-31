from unittest.mock import patch

from classes.SetAction import SetAction
import pytest


def test_validate_given_one_empty_str_throws() -> None:
    action = SetAction("", "10")
    with pytest.raises(ValueError):
        action.validate()


def test_validate_given_str_with_spaces_throws() -> None:
    action = SetAction("a b", "10")
    with pytest.raises(ValueError):
        action.validate()


def test_validate_given_both_invalid_str_throws() -> None:
    action = SetAction("a a", "b b")
    with pytest.raises(ValueError):
        action.validate()


def test_validate_given_both_valid_str_not_throws() -> None:
    action = SetAction("a", "10")
    try:
        action.validate()
    except ValueError:
        assert False


@patch("db.db_operations.get_key_value_by_key")
@patch("db.db_operations.datastore_client")
def test_set_first_key_return_key_and_none_value(mock_client, mock_get_by_key):
    mock_get_by_key.return_value = ('a', 'None')
    action = SetAction('a', '10')

    key, value = action.execute()

    assert (key == 'a' and value == 'None')


@patch("db.db_operations.get_key_value_by_key")
@patch("db.db_operations.datastore_client")
def test_set_key_return_key_and_value(mock_client, mock_get_by_key):
    mock_get_by_key.return_value = ('a', '30')
    action = SetAction('a', '10')

    key, value = action.execute()

    assert (key == 'a' and value == '30')



