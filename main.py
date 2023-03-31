import logging
from flask import Flask, render_template, request

from classes.HistoryChanges import HistoryChanges
from classes.WebActionFactory import WebActionFactory
from utiles.constants import HTML_PATH, NAME_PARAMETER, VALUE_PARAMETER, NONE_STR, CLEANED_STR

app = Flask(__name__)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

action_factory = WebActionFactory()

history_changes = HistoryChanges()


@app.route('/')
def root() -> str:
    return render_template(HTML_PATH)


@app.route('/set')
def set_variable() -> str:
    error_message = None
    output = None
    variable_name = request.args.get(NAME_PARAMETER)
    variable_value = request.args.get(VALUE_PARAMETER)
    action = action_factory.get_action(action_type='set', variable_name=variable_name, variable_value=variable_value)
    try:
        action.validate()
    except ValueError as ex:
        logger.error(f'Invalid input: {variable_name}')
        error_message = str(ex)
        return render_template(HTML_PATH, output=output, error_message=error_message)

    key, old_value = action.execute()
    history_changes.push(key, old_value)
    output = f'{variable_name} = {variable_value}'
    return render_template(HTML_PATH, output=output, error_message=error_message)


@app.route('/get')
def get() -> str:
    variable_name = request.args.get(NAME_PARAMETER)
    action = action_factory.get_action(action_type='get', variable_name=variable_name)
    output = action.execute()

    return render_template(HTML_PATH, output=output)


@app.route('/unset')
def unset() -> str:
    variable_name = request.args.get(NAME_PARAMETER)
    action = action_factory.get_action(action_type='unset', variable_name=variable_name)

    key, old_value = action.execute()
    history_changes.push(key, old_value)
    output = f'{variable_name} = {NONE_STR}'
    return render_template(HTML_PATH, output=output)


@app.route('/numequalto')
def num_equal_to() -> str:
    variable_value = request.args.get(VALUE_PARAMETER)
    action = action_factory.get_action(action_type='numequalto', variable_value=variable_value)
    output = action.execute()

    return render_template(HTML_PATH, output=output)


@app.route('/undo')
def undo() -> str:
    output = history_changes.undo()
    return render_template(HTML_PATH, output=output)


@app.route('/redo')
def redo() -> str:
    output = history_changes.redo()
    return render_template(HTML_PATH, output=output)


@app.route('/end')
def end() -> str:
    action = action_factory.get_action(action_type='end')
    action.execute()
    history_changes.clear()
    return render_template(HTML_PATH, output=CLEANED_STR)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
