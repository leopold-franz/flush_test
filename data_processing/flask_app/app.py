from flask import request, url_for
import json
import jsonschema

from data_processing.flask_app import create_app
from data_processing.busines_logic.service import list_raw_measurements, process_raw_measurements

app = create_app()
database_connection = {}
with open('data_processing/flask_app/config/schema.json') as json_file:
    raw_data_schema = json.load(json_file)


def validate_json(json_data):
    try:
        jsonschema.validate(instance=json_data, schema=raw_data_schema)
    except jsonschema.exceptions.ValidationError as err:
        return False
    return True


@app.route('/measurement', methods=['POST'])
def process_raw_data():
    data = request.get_json(force=True)
    assert validate_json(data), 'POST body failed to validate against own raw_data schema'
    result = process_raw_measurements(database_connection['cursor'], data)
    return str(result)


@app.route('/measurement', methods=['GET'])
def show_data():
    result = list_raw_measurements(database_connection['cursor'])
    return str(result)


def run_app(cursor):
    database_connection['cursor'] = cursor
    app.run(host='0.0.0.0', port=8080)


# with app.test_request_context():
#     print(url_for('get_sensor_data'))

if __name__ == '__main__':
    run_app()
