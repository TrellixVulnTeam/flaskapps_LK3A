# -*- coding: utf-8 -*-
"""
api.account.py
~~~~~~

:copyright: (c) 2014 by @zizzamia
:license: BSD (See LICENSE for details)
"""
from flask import Blueprint, request, g
from werkzeug import secure_filename

# Imports inside Bombolone
import bombolone.core.users
from bombolone.core.utils import jsonify
from bombolone.decorators import authentication, get_hash, check_rank

api_account = Blueprint('api_account', __name__)

@api_account.route('/api/1.0/account/update.json', methods=['POST'])
@authentication
@check_rank(10)
@get_hash('users')
def update():
    """ 
    """
    params = request.json
    user_id = params["_id"]
    data = core.users.update(user_id=user_id, params=params)
    return jsonify(data)

@api_account.route('/api/1.0/account/update_profile.json', methods=['POST'])
@authentication
@get_hash('users')
def update_profile():
    """ 
    """
    params = request.json
    user_id = g.my['_id']
    data = core.users.update_profile(user_id=user_id, params=params)
    return jsonify(data)

@api_account.route('/api/1.0/account/update_account.json', methods=['POST'])
@authentication
@get_hash('users')
def update_account():
    """ 
    """
    params = request.json
    user_id = g.my['_id']
    data = core.users.update_account(user_id=user_id, params=params)
    return jsonify(data)

@api_account.route('/api/1.0/account/update_password.json', methods=['POST'])
@authentication
@get_hash('users')
def update_password():
    """ 
    """
    params = request.json
    user_id = g.my['_id']
    data = core.users.update_password(user_id=user_id, params=params)
    return jsonify(data)

@api_account.route('/api/1.0/account/upload_avatar.json', methods=['POST'])
@authentication
@get_hash('users')
def upload_avatar():
    """ """
    name = secure_filename(request.headers.get('X-File-Name'))
    data = core.users.upload_avatar(name=name)
    return jsonify(data)
