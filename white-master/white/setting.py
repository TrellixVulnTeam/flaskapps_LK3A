#!/usr/bin/env python
# 2015 Copyright (C) White
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


class Config:

    HOST = 'localhost' # server host
    PORT = 5000 # server port

    DEBUG = True # open debug mode

    # csrf protect
    # CSRF_SECRET = 'fRLoWItHQQajq//4ebYUDewXVF2B9UEznoVD7kC7D9o='

    # Flask Session module
    # session
    # SECRET_KEY = '7oGwHH8NQDKn9hL12Gak9G/MEjZZYk4PsAxqKU4cJoY='
    # SESSION_TYPE = 'filesystem'
    # SESSION_FILE_DIR = '/var/www/$yoursite.com/cookies'
    # SESSION_FILE_THRESHOLD = 100
    # SESSION_FILE_MODE = 0600
    
    ######
    # Wanna use redis session, please comment filesystem session settings
    # SESSION_TYPE = 'redis'
    # 
    # REDIS_HOST = localhost
    # PERMANENT_SESSION_LIFETIME = 60

    # DB Config
    DB_CONFIG = {
        'db': 'white',
        'user': 'white',
        'passwd': 'white',
        'host': 'localhost',

        'max_idle': 10  # the mysql timeout setting
    }
    DB_MAXCONN = 10
    DB_MINCONN = 5

    # the custom fields asset path
    CONTENT_PATH = '/var/www/$yoursite.com/content'

    LANGUAGE = 'en_GB'  # in ('zh_CN', 'zh_TW', 'en_GB')

    THEME = 'default'  # the froent theme name
