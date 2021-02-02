'''

This file will test the following cases:
  - retrieving all prediction titles, with respect to a supplied userid.

Note: the 'pytest' instances can further be reviewed:

    - https://pytest-flask.readthedocs.io/en/latest
    - http://docs.pytest.org/en/latest/usage.html

'''

import json
import os.path
import datetime
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
            'results',
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


def test_retrieve_titles(client, live_server, token):
    '''

    This method retrieves all prediction titles, with respect to an
    identified userid (i.e. uid).

    '''

    @live_server.app.route('/retrieve-prediction-titles')
    def retrieve_prediction_titles():
        return url_for('api.retrieve_prediction_titles', _external=True)

    live_server.start()

    # local variables
    endpoint = retrieve_prediction_titles()

    res = send_post(
        client,
        endpoint,
        token,
        get_sample_json('retrieve-titles.json', 'combined')
    )

    # assertion checks
    assert res.status_code == 200

    if res.json['status'] == 1:
        print 'Unsuccessful retrieval of prediction titles'
        assert False
    elif res.json['status'] == 2:
        print 'Improper request submitted.'
        assert False
    else:
        assert res.json['status'] == 0

    try:
        date_svm = res.json['titles'][0][2]
        date_svr = res.json['titles'][1][2]
        datetime.datetime.strptime(date_svm, '%Y-%m-%d %H:%M:%S')
        datetime.datetime.strptime(date_svr, '%Y-%m-%d %H:%M:%S')

        if (
            [1, 'svm-prediction-1', date_svm] == res.json['titles'][0] and
            [2, 'svr-prediction-1', date_svr] == res.json['titles'][1]
        ):
            assert True
        else:
            assert False

    except:
        assert False
