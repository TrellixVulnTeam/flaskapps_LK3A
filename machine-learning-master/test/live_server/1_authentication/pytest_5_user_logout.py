'''

This file will test the necessary interfaces required to logout.

Note: the 'pytest' instances can further be reviewed:

    - https://pytest-flask.readthedocs.io/en/latest
    - http://docs.pytest.org/en/latest/usage.html

'''

import json


def test_logout(client, live_server):
    '''

    This method tests the user logout process. It seems redundant, since it
    requires executing the login session. However, this login session is not
    identical to the login session test, which covers testing the username,
    and password requirements, along with the password hashing function. This
    test simply assumes the latter conditions have been met, and proceeds to
    testing if the logout would succeed, given the user can login.

    '''

    live_server.start()

    # local variables
    username = 'jeff1evesque'
    password = 'password123'
    payload = {'user[login]': username, 'user[password]': password}

    # post requests: login, and logout response
    login = client.post(
        '/login',
        headers={'Content-Type': 'application/json'},
        data=json.dumps(payload)
    )
    token = login.json['access_token']

    if token:
        logout = client.post(
            '/logout',
            headers={'Authorization': 'Bearer {0}'.format(token)}
        )
    else:
        assert False

    # assertion checks
    assert login.status_code == 200
    assert login.json['status'] == 0
    assert token
    assert logout.status_code == 200
    assert logout.json['status'] == 0
