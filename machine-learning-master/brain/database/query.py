#!/usr/bin/python

'''

This file contains various SQL, and NoSql related methods.

'''

from flask import g
import MySQLdb as MariaClient
from pymongo import MongoClient, errors
from brain.database.settings import Database


def get_mariadb(host, user, passwd, database):
    '''

    This function opens a new mariadb database connection, if there is none yet
    for the current application context.

    Note: the following resources can be further reviewed:

          http://flask.pocoo.org/docs/0.12/tutorial/dbcon/
          http://flask.pocoo.org/docs/0.12/appcontext/#context-usage

    '''

    if not hasattr(g, 'mariadb'):
        if database is None:
            conn = MariaClient.connect(host, user, passwd)

        else:
            conn = MariaClient.connect(host, user, passwd, database)

        g.mariadb = conn

    return g.mariadb


def get_mongodb():
    '''

    This function opens a new mongo database connection, if there is none yet
    for the current application context.

    Note: the following resources can be further reviewed:

          http://flask.pocoo.org/docs/0.12/tutorial/dbcon/
          http://flask.pocoo.org/docs/0.12/appcontext/#context-usage

    '''

    if not hasattr(g, 'mongodb'):
        settings = Database()
        params = {
            'user': settings.get_db_username('nosql'),
            'pass': settings.get_db_password('nosql'),
            'host': settings.get_db_host('nosql'),
        }

        client = MongoClient(
            "mongodb://{user}:{pass}@{host}/admin?authSource=admin".format(**params)
        )
        g.mongodb = client

    return g.mongodb


class NoSQL(object):
    '''

    This class provides an interface to connect, execute commands, and
    disconnect from a NoSQL database.

    Note: this class explicitly inherits the 'new-style' class.

    '''

    def __init__(self):
        '''

        This constructor is responsible for defining class variables.

        '''

        self.list_error = []
        self.proceed = True
        self.client = get_mongodb()

    def connect(self, collection=None):
        '''

        This method is responsible for defining the necessary interface to
        connect to a NoSQL database, using an established mongod client.

        '''

        try:
            # single mongodb instance
            database = Database().get_db('nosql')
            self.database = self.client[database]

            if collection:
                self.collection = self.database[collection]

            return {
                'status': True,
                'error': None,
            }

        except errors, error:
            self.proceed = False
            self.list_error.append(error)

            return {
                'status': False,
                'error': self.list_error,
            }

    def execute(self, operation, payload):
        '''

        This method is responsible for defining the necessary interface to
        perform NoSQL commands.

        Note: collection level operations can be further reviewed:

          - http://api.mongodb.com/python/current/api/pymongo/collection.html

        '''

        result = None
        if self.proceed:
            try:
                if operation == 'aggregate':
                    result = self.collection.aggregate(payload)
                elif operation == 'insert_one':
                    result = self.collection.insert_one(payload)
                elif operation == 'insert_many':
                    result = self.collection.insert_many(payload)
                elif operation == 'update_one':
                    result = self.collection.update_one(payload)
                elif operation == 'update_many':
                    result = self.collection.update_many(payload)
                elif operation == 'delete_one':
                    result = self.collection.delete_one(payload)
                elif operation == 'delete_many':
                    result = self.collection.delete_many(payload)
                elif operation == 'find':
                    result = self.collection.find(payload)
                elif operation == 'map_reduce':
                    result = self.collection.map_reduce(
                        payload['map'],
                        payload['reduce'],
                        payload['out'],
                        payload['full_response'],
                        payload['kwargs']
                    )
                elif operation == 'delete_one':
                    result = self.collection.delete_one(payload)
                elif operation == 'delete_many':
                    result = self.collection.delete_many(payload)
                elif operation == 'count_documents':
                    if payload:
                        result = self.collection.find(payload).count()
                    else:
                        result = self.collection.count()
                elif operation == 'drop_collection':
                    result = self.database.drop_collection(payload)

            except errors, error:
                self.list_error.append(error)

                return {
                    'status': False,
                    'result': result,
                    'error': self.list_error,
                }

            if result:
                return {'status': True, 'result': result, 'error': None}
            else:
                return {'status': False, 'result': None, 'error': None}

    def disconnect(self):
        '''
        This method is responsible for defining the necessary interface to
        disconnect from a NoSQL database.
        '''

        if self.proceed:
            try:
                self.client.close()

                return {
                    'status': True,
                    'error': None,
                }

            except errors, error:
                self.list_error.append(error)

                return {
                    'status': False,
                    'error': self.list_error,
                }

    def get_errors(self):
        '''

        This method returns all errors pertaining to the instantiated class.

        '''

        return self.list_error


class SQL(object):
    '''

    This class provides an interface to connect, execute commands, and
    disconnect from a SQL database.

    Note: this class explicitly inherits the 'new-style' class.

    '''

    def __init__(self, host=None, user=None, passwd=None):
        '''

        This constructor is responsible for defining class variables.

        '''

        self.settings = Database()
        self.list_error = []
        self.proceed = True

        # host address
        if host:
            self.host = host
        else:
            self.host = self.settings.get_db_host('sql')

        # username for above host address
        if user:
            self.user = user
        else:
            self.user = self.settings.get_db_username('sql')

        # password for above username
        if passwd:
            self.passwd = passwd
        else:
            self.passwd = self.settings.get_db_password('sql')

    def connect(self, database=None):
        '''

        This method is responsible for defining the necessary interface to
        connect to a SQL database.

        '''

        self.conn = get_mariadb(self.host, self.user, self.passwd, database)
        self.cursor = self.conn.cursor()

    def execute(self, operation, statement, sql_args=None):
        '''

        This method is responsible for defining the necessary interface to
        perform SQL commands.

        @sql_args, is a tuple used for argument substitution with the supplied
            'statement'.

        '''

        if self.proceed:
            try:
                self.cursor.execute(statement, sql_args)

                # commit change(s), return lastrowid
                if operation in ['insert', 'delete', 'update']:
                    self.conn.commit()

                    return {
                        'status': True,
                        'error': self.list_error,
                        'id': self.cursor.lastrowid,
                    }

                # fetch all the rows, return as list of lists.
                elif operation == 'select':
                    result = self.cursor.fetchall()

                    return {
                        'status': True,
                        'error': self.list_error,
                        'result': result,
                    }

            except MariaClient.Error, error:
                self.conn.rollback()
                self.list_error.append(error)

                return {
                    'status': False,
                    'error': self.list_error,
                    'result': None,
                }

    def disconnect(self):
        '''

        This method is responsible for defining the necessary interface to
        disconnect from a SQL database.

        '''

        if self.proceed:
            try:
                if self.conn:
                    self.conn.close()

                    return {
                        'status': True,
                        'error': None,
                        'id': self.cursor.lastrowid,
                    }

            except MariaClient.Error, error:
                self.list_error.append(error)

                return {
                    'status': False,
                    'error': self.list_error,
                    'id': self.cursor.lastrowid,
                }

    def get_errors(self):
        '''

        This method returns all errors pertaining to the instantiated class.

        '''

        return self.list_error
