from flask import Flask, render_template, request

from db.db_operations import store_variable, get_variable_value
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

    print(f'Output = {output}\n Error = {error_message}')
    return render_template('index.html', output=output, error_message=error_message)


@app.route('/get')
def get() -> str:
    output = None
    variable_name = request.args.get('name')
    output = get_variable_value(variable_name)
    print(f'Output = {output}')
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
