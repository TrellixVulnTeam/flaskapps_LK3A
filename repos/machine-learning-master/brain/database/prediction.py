#!/usr/bin/python

'''

This file saves, as well as retrieves, previous stored predictions.

'''

from flask import current_app, session
from brain.database.query import SQL


class Prediction(object):
    '''

    This class provides an interface to save, or retrieve, a previously
    generated svm or, svr prediction result.

    Note: this class explicitly inherits the 'new-style' class.

    '''

    def __init__(self):
        '''

        This constructor is responsible for defining class variables.

        '''

        self.list_error = []
        self.sql = SQL()
        self.db_ml = current_app.config.get('SQL_DB')
        self.model_list = current_app.config.get('MODEL_TYPE')

        if session.get('uid'):
            self.uid = int(session.get('uid'))
        else:
            self.uid = 0

    def save(self, data, model_type, title):
        '''

        This method stores the corresponding prediction.

        @sql_statement, is a sql format string, and not a python string.
            Therefore, '%s' is used for argument substitution.

        Note: 'UTC_TIMESTAMP' returns the universal UTC datetime

        '''

        # local variables
        result = data['result']

        # insert prediction
        self.sql.connect(self.db_ml)

        if model_type == 'svm':
            classes = data['classes']
            probability = data['probability']
            decision_function = data['decision_function']

            # svm results
            sql_statement = 'INSERT INTO tbl_prediction_results '\
                '(model_type, title, result, uid_created, datetime_created) '\
                'VALUES(%s, %s, %s, %s, UTC_TIMESTAMP())'
            args = (self.model_list.index(model_type) + 1, title, result, self.uid)
            svm_results = self.sql.execute('insert', sql_statement, args)

            # svm classes
            for x in classes:
                sql_statement = 'INSERT INTO tbl_svm_results_class '\
                    '(id_result, class) VALUES(%s, %s)'
                args = (svm_results['id'], x)
                self.sql.execute('insert', sql_statement, args)

            # svm probability
            for x in probability:
                sql_statement = 'INSERT INTO tbl_svm_results_probability '\
                    '(id_result, probability) VALUES(%s, %s)'
                args = (svm_results['id'], x)
                self.sql.execute('insert', sql_statement, args,)

            # svm decision function
            for x in decision_function:
                sql_statement = 'INSERT INTO tbl_svm_results_decision_function '\
                    '(id_result, decision_function) VALUES(%s, %s)'
                args = (svm_results['id'], x,)
                self.sql.execute('insert', sql_statement, args,)

        elif model_type == 'svr':
            # svr results
            sql_statement = 'INSERT INTO tbl_prediction_results '\
                '(model_type, title, result, uid_created, datetime_created) '\
                'VALUES(%s, %s, %s, %s, UTC_TIMESTAMP())'
            args = (self.model_list.index(model_type) + 1, title, result, self.uid)
            svr_results = self.sql.execute('insert', sql_statement, args,)

            # svr r2
            sql_statement = 'INSERT INTO tbl_svr_results_r2 '\
                '(id_result, r2) VALUES(%s, %s)'
            args = (svr_results['id'], data['r2'])
            self.sql.execute('insert', sql_statement, args,)

        # retrieve any error(s)
        response_error = self.sql.get_errors()

        # return result
        if response_error:
            return {'error': response_error, 'result': 1}
        else:
            return {'error': None, 'result': 0}

    def get_all_titles(self, model_type=None):
        '''

        This method retrieves all stored predictions for the current user.

        @model_type, constrains the 'select' result to a specified model type.
            Otherwise, defaults to return results for all model types.

        @sql_statement, is a sql format string, and not a python string.
            Therefore, '%s' is used for argument substitution.

        '''

        # select prediction
        self.sql.connect(self.db_ml)

        if model_type in self.model_list:
            sql_statement = 'SELECT id_result, title, datetime_created ' \
                'FROM tbl_prediction_results '\
                'WHERE uid_created=%s '\
                'AND model_type=%s'
            args = (self.uid, self.model_list.index(model_type) + 1)
            response = self.sql.execute('select', sql_statement, args)

        elif model_type == 'all':
            sql_statement = 'SELECT id_result, title, datetime_created '\
                'FROM tbl_prediction_results '\
                'WHERE uid_created=%s'
            args = (self.uid)
            response = self.sql.execute('select', sql_statement, args)

        # retrieve any error(s)
        response_error = self.sql.get_errors()

        # return result
        if response_error:
            return {
                'status': False,
                'error': response_error,
                'result': None
            }
        else:
            return {
                'status': True,
                'error': None,
                'result': response['result'],
            }

    def get_result(self, id_result):
        '''

        This method retrieves a prediction result, based on the supplied
            id_result.

        @sql_statement, is a sql format string, and not a python string.
            Therefore, '%s' is used for argument substitution.

        '''

        # select result
        self.sql.connect(self.db_ml)

        sql_statement = 'SELECT result FROM tbl_prediction_results '\
            'WHERE id_result=%s'
        args = (id_result,)
        response = self.sql.execute('select', sql_statement, args)

        # retrieve any error(s)
        response_error = self.sql.get_errors()

        # return result
        if response_error:
            return {
                'status': False,
                'error': response_error,
                'result': None
            }
        else:
            return {
                'status': True,
                'error': None,
                'result': response['result'],
            }

    def get_model_type(self, id_result):
        '''

        This method retrieves the 'model_type' name given the 'id_result'.

        @sql_statement, is a sql format string, and not a python string.
            Therefore, '%s' is used for argument substitution.

        '''

        # select parameter
        self.sql.connect(self.db_ml)

        sql_statement = 'SELECT model FROM tbl_model_type '\
            'WHERE id_model '\
            'IN (SELECT model_type '\
            'FROM tbl_prediction_results '\
            'WHERE id_result=%s)'
        args = (id_result,)
        response = self.sql.execute('select', sql_statement, args)

        # retrieve any error(s)
        response_error = self.sql.get_errors()

        # return result
        if response_error:
            return {
                'status': False,
                'error': response_error,
                'result': None
            }

        else:
            return {
                'status': False,
                'error': 'No sql logic executed',
                'result': response['result'][0][0]
            }

    def get_value(self, id_result, model_type, param):
        '''

        This method retrieves a specified param, with respect to a supplied
            id_result, and 'model_type', for a given prediction result.

        @model_type, constrains the 'select' result to a specified model type.

        @param, specifies which table, and corresponding column parameter to
            query, and select from:

            - class: requires svm 'model_type'
            - decision_function: requires svm 'model_type'
            - probability: requires svm 'model_type'
            - r2: requires svr 'model_type'

        @sql_statement, is a sql format string, and not a python string.
            Therefore, '%%s' is used for argument substitution.

        '''

        # select parameter
        self.sql.connect(self.db_ml)

        if model_type in self.model_list:
            if param in ['class', 'decision_function', 'probability', 'r2']:
                sql_statement = 'SELECT %s FROM tbl_%s_results_%s '\
                    'WHERE id_result=%%s' % (param, model_type, param)
                args = (id_result,)
                response = self.sql.execute('select', sql_statement, args)

                return {
                    'status': True,
                    'error': None,
                    'result': response['result'],
                }

        # retrieve any error(s)
        response_error = self.sql.get_errors()

        # return result
        if response_error:
            return {
                'status': False,
                'error': response_error,
                'result': None
            }

        else:
            return {
                'status': False,
                'error': 'No sql logic executed',
                'result': None
            }
