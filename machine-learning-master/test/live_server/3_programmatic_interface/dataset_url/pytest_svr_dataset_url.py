'''

This file will test the following svr sessions:

  - data_new: stores supplied dataset into a SQL database.
  - data_append: appends supplied dataset to an already stored dataset in an
                 SQL database.
  - model_generate: generate an model by selecting a particular range of
                    dataset (session), and store it into a NoSQL cache.
  - model_predict: generate a prediction by selecting a particular cached
                   model from the NoSQL cache.

Note: the 'pytest' instances can further be reviewed:

    - https://pytest-flask.readthedocs.io/en/latest
    - http://docs.pytest.org/en/latest/usage.html

'''

import json
import os.path
from flask import current_app, url_for


def get_sample_json(jsonfile, model_type):
    '''

    Get a sample json dataset.

    '''

    # local variables
    root = current_app.config.get('ROOT')

    # open file
    json_dataset = None

    with open(
        os.path.join(
            root,
            'interface',
            'static',
            'data',
            'json',
            'programmatic_interface',
            model_type,
            'dataset_url',
            jsonfile
        ),
        'r'
    ) as json_file:
        json_dataset = json.load(json_file)

    return json.dumps(json_dataset)


def send_post(client, endpoint, token, data):
    '''

    This method will login, and return the corresponding token.

    @token, is defined as a fixture, in our 'conftest.py', to help reduce
        runtime on our tests.

    '''

    return client.post(
        endpoint,
        headers={
            'Authorization': 'Bearer {0}'.format(token),
            'Content-Type': 'application/json'
        },
        data=data
    )


def test_data_new(client, live_server, token):
    '''

    This method tests the 'data_new' session.

    '''

    @live_server.app.route('/load-data')
    def load_data():
        return url_for('api.load_data', _external=True)

    live_server.start()

    # local variables
    endpoint = load_data()

    res = send_post(
        client,
        endpoint,
        token,
        get_sample_json('svr-data-new.json', 'svr')
    )

    # assertion checks
    assert res.status_code == 200
    assert res.json['status'] == 0


def test_data_append(client, live_server, token):
    '''

    This method tests the 'data_new' session.

    '''

    @live_server.app.route('/load-data')
    def load_data():
        return url_for('api.load_data', _external=True)

    live_server.start()

    # local variables
    endpoint = load_data()

    res = send_post(
        client,
        endpoint,
        token,
        get_sample_json('svr-data-append.json', 'svr')
    )

    # assertion checks
    assert res.status_code == 200
    assert res.json['status'] == 0


def test_model_generate(client, live_server, token):
    '''

    This method tests the 'model_generate' session.

    '''

    @live_server.app.route('/load-data')
    def load_data():
        return url_for('api.load_data', _external=True)

    live_server.start()

    # local variables
    endpoint = load_data()

    res = send_post(
        client,
        endpoint,
        token,
        get_sample_json('svr-model-generate.json', 'svr')
    )

    # assertion checks
    assert res.status_code == 200
    assert res.json['status'] == 0


def test_model_predict(client, live_server, token):
    '''

    This method tests the 'model_predict' session.

    Note: for debugging, the following syntax will output the corresponding
          json values, nested within 'json.loads()', to the travis ci:

          raise ValueError(res.json['result']['key1'])

    '''

    @live_server.app.route('/load-data')
    def load_data():
        return url_for('api.load_data', _external=True)

    live_server.start()

    # local variables
    endpoint = load_data()

    res = send_post(
        client,
        endpoint,
        token,
        get_sample_json('svr-model-predict.json', 'svr')
    )

    # assertion checks
    assert res.status_code == 200
    assert res.json['status'] == 0
    assert res.json['result']
    assert res.json['result']['confidence']
    assert res.json['result']['confidence']['score'] == '0.29007217517499473'
    assert res.json['result']['model'] == 'svr'
    assert res.json['result']['result'] == '37.7622192912'
