from utiles.validations import validate_input


def test_validate_input() -> None:
    assert validate_input("a")
    assert validate_input("variable")
    assert not validate_input("")
    assert not validate_input("variable with spaces")


