from flask import Flask, render_template, request
from collections import deque
from db.db_operations import store_variable, get_entity_by_key, get_entities_by_value, delete_entity_by_key, \
    delete_all_entities
from utiles.constants import HTML_PATH, NAME_PARAMETER, VALUE_PARAMETER, VALUE_ATTRIBUTE, NONE_STR, NO_COMMANDS_STR, \
    CLEANED_STR
from utiles.validations import validate_input

app = Flask(__name__)


undo_stack = deque()
redo_stack = deque()


@app.route('/')
def root() -> str:
    return render_template(HTML_PATH)


@app.route('/set')
def set_variable() -> str:
    error_message = None
    output = None
    variable_name = request.args.get(NAME_PARAMETER)
    variable_value = request.args.get(VALUE_PARAMETER)
    try:
        if not validate_input(variable_name) or not validate_input(variable_value):
            raise ValueError("name and value variables must not be empty and not contain any spaces.")
        output = f'{variable_name} = {variable_value}'
        entity = get_entity_by_key(variable_name)
        store_variable(variable_name, variable_value)
        if entity:
            old_value = entity[VALUE_ATTRIBUTE]
        else:
            old_value = NONE_STR
        undo_stack.append((variable_name, old_value))
    except ValueError as ex:
        error_message = str(ex)
    return render_template(HTML_PATH, output=output, error_message=error_message)


@app.route('/get')
def get() -> str:
    variable_name = request.args.get(NAME_PARAMETER)
    entity = get_entity_by_key(variable_name)
    if entity:
        output = entity[VALUE_ATTRIBUTE]
    else:
        output = NONE_STR

    return render_template(HTML_PATH, output=output)


@app.route('/unset')
def unset() -> str:
    variable_name = request.args.get(NAME_PARAMETER)
    entity = get_entity_by_key(variable_name)

    if entity:
        old_value = entity[VALUE_ATTRIBUTE]
        undo_stack.append((variable_name, old_value))

    delete_entity_by_key(variable_name)
    output = f'{variable_name} = {NONE_STR}'
    return render_template(HTML_PATH, output=output)


@app.route('/numequalto')
def num_equal_to() -> str:
    variable_value = request.args.get(VALUE_PARAMETER)
    output = str(len(get_entities_by_value(variable_value)))
    return render_template(HTML_PATH, output=output)


@app.route('/undo')
def undo() -> str:
    output = NO_COMMANDS_STR
    if undo_stack:
        variable_name, variable_value = undo_stack.pop()
        entity = get_entity_by_key(variable_name)
        if entity:
            old_value = entity[VALUE_ATTRIBUTE]
        else:
            old_value = NONE_STR
        redo_stack.append((variable_name, old_value))
        if variable_value == NONE_STR:
            delete_entity_by_key(variable_name)
        else:
            store_variable(variable_name, variable_value)
        output = f'{variable_name} = {variable_value}'
    return render_template(HTML_PATH, output=output)


@app.route('/redo')
def redo() -> str:
    output = NO_COMMANDS_STR
    if redo_stack:
        variable_name, variable_value = redo_stack.pop()
        if variable_value == NONE_STR:
            delete_entity_by_key(variable_name)
        else:
            store_variable(variable_name, variable_value)

        output = f'{variable_name} = {variable_value}'

    return render_template(HTML_PATH, output=output)


@app.route('/end')
def end() -> str:
    delete_all_entities()
    undo_stack.clear()
    redo_stack.clear()
    output = CLEANED_STR
    return render_template(HTML_PATH, output=output)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
