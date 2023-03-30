from flask import Flask, render_template, request

from db.db_operations import store_variable, get_entity_by_key, get_entities_by_value, delete_entity_by_key, \
    delete_all_entities
from utiles.validations import validate_input

app = Flask(__name__)


@app.route('/')
def root() -> str:
    return render_template('index.html')


@app.route('/set')
def set_variable() -> str:
    error_message = None
    output = None
    variable_name = request.args.get('name')
    variable_value = request.args.get('value')
    try:
        if not validate_input(variable_name) or not validate_input(variable_value):
            raise ValueError("name and value variables must not be empty and not contain any spaces.")
        output = f'{variable_name} = {variable_value}'
        store_variable(variable_name, variable_value)
    except ValueError as ex:
        error_message = str(ex)

    return render_template('index.html', output=output, error_message=error_message)


@app.route('/get')
def get() -> str:
    variable_name = request.args.get('name')
    entity = get_entity_by_key(variable_name)
    if entity:
        output = entity['value']
    else:
        output = 'None'

    return render_template('index.html', output=output)


@app.route('/unset')
def unset() -> str:
    variable_name = request.args.get('name')
    delete_entity_by_key(variable_name)
    output = f'{variable_name} = None'
    return render_template('index.html', output=output)


@app.route('/numequalto')
def num_equal_to() -> str:
    variable_value = request.args.get('value')
    output = str(len(get_entities_by_value(variable_value)))
    return render_template('index.html', output=output)


@app.route('/end')
def end() -> str:
    delete_all_entities()
    output = "CLEANED"
    return render_template('index.html', output=output)


if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
