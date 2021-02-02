from importlib import reload
import inspect
import json
import os
import sys
import unittest

import pytest
from bugsnag.configuration import Configuration
from bugsnag.event import Event
from tests import fixtures


class TestEvent(unittest.TestCase):
    event_class = Event

    def test_sanitize(self):
        """
            It should sanitize request data
        """
        config = Configuration()
        event = self.event_class(Exception("oops"), config, {},
                                 request={"params": {"password": "secret"}})

        event.add_tab("request", {"arguments": {"password": "secret"}})

        payload = json.loads(event._payload())
        request = payload['events'][0]['metaData']['request']
        self.assertEqual(request['arguments']['password'], '[FILTERED]')
        self.assertEqual(request['params']['password'], '[FILTERED]')

    def test_code(self):
        """
            It should include code
        """
        config = Configuration()
        line = inspect.currentframe().f_lineno + 1
        event = self.event_class(Exception("oops"), config, {})

        payload = json.loads(event._payload())

        code = payload['events'][0]['exceptions'][0]['stacktrace'][0]['code']
        lvl = "        "
        self.assertEqual(code[str(line - 3)], lvl + "\"\"\"")
        self.assertEqual(code[str(line - 2)], lvl + "config = Configuration()")
        self.assertEqual(code[str(line - 1)],
                         lvl + "line = inspect.currentframe().f_lineno + 1")
        self.assertEqual(
            code[str(line)],
            lvl +
            "event = self.event_class(Exception(\"oops\"), config, {})"
            )
        self.assertEqual(code[str(line + 1)], "")
        self.assertEqual(code[str(line + 2)],
                         lvl + "payload = json.loads(event._payload())")
        self.assertEqual(code[str(line + 3)], "")

    def test_code_at_start_of_file(self):

        config = Configuration()
        event = self.event_class(fixtures.start_of_file[1], config, {},
                                 traceback=fixtures.start_of_file[2])

        payload = json.loads(event._payload())

        code = payload['events'][0]['exceptions'][0]['stacktrace'][0]['code']
        self.assertEqual(
            {'1': '# flake8: noqa',
             '2': 'try:',
             '3': '    import sys; raise Exception("start")',
             '4': 'except Exception: start_of_file = sys.exc_info()',
             '5': '# 4',
             '6': '# 5',
             '7': '# 6'}, code)

    def test_code_at_end_of_file(self):

        config = Configuration()
        event = self.event_class(fixtures.end_of_file[1], config, {},
                                 traceback=fixtures.end_of_file[2])

        payload = json.loads(event._payload())

        code = payload['events'][0]['exceptions'][0]['stacktrace'][0]['code']
        self.assertEqual(
            {'6':  '# 5',
             '7':  '# 6',
             '8':  '# 7',
             '9':  '# 8',
             '10': 'try:',
             '11': '    import sys; raise Exception("end")',
             '12': 'except Exception: end_of_file = sys.exc_info()'}, code)

    def test_code_turned_off(self):
        config = Configuration()
        config.send_code = False
        event = self.event_class(Exception("oops"), config, {},
                                 traceback=fixtures.end_of_file[2])

        payload = json.loads(event._payload())

        code = payload['events'][0]['exceptions'][0]['stacktrace'][0]['code']
        self.assertEqual(code, None)

    def test_no_traceback_exclude_modules(self):
        from tests.fixtures import helpers
        config = Configuration()
        config.configure(project_root=os.path.join(os.getcwd(), 'tests'))

        event = helpers.invoke_exception_on_other_file(config)

        payload = json.loads(event._payload())
        exception = payload['events'][0]['exceptions'][0]
        first_traceback = exception['stacktrace'][0]

        self.assertEqual(first_traceback['file'], 'fixtures/helpers.py')
        self.assertEqual(
            {
                '1': 'def invoke_exception_on_other_file(config):',
                '2': '    from bugsnag.event import Event',
                '3': '',
                '4': '    return Event(Exception("another file!"), config, {})'
            },
            first_traceback['code']
        )

    def test_traceback_exclude_modules(self):
        # Make sure samples.py is compiling to pyc
        import py_compile
        py_compile.compile('./tests/fixtures/helpers.py')

        from tests.fixtures import helpers
        reload(helpers)  # .py variation might be loaded from previous test.

        if sys.version_info < (3, 0):
            # Python 2.6 & 2.7 returns the cached file on __file__,
            # and hence we verify it returns .pyc for these versions
            # and the code at _generate_stacktrace() handles that.
            self.assertTrue(helpers.__file__.endswith('.pyc'))

        config = Configuration()
        config.configure(project_root=os.path.join(os.getcwd(), 'tests'))
        config.traceback_exclude_modules = [helpers]

        event = helpers.invoke_exception_on_other_file(config)

        payload = json.loads(event._payload())
        exception = payload['events'][0]['exceptions'][0]
        first_traceback = exception['stacktrace'][0]
        self.assertEqual(first_traceback['file'], 'test_event.py')

    def test_device_data(self):
        """
            It should include device data
        """
        config = Configuration()
        config.hostname = 'test_host_name'
        config.runtime_versions = {'python': '9.9.9'}
        event = self.event_class(Exception("oops"), config, {})

        payload = json.loads(event._payload())

        device = payload['events'][0]['device']
        self.assertEqual('test_host_name', device['hostname'])
        self.assertEqual('9.9.9', device['runtimeVersions']['python'])

    def test_default_app_type(self):
        """
        app_type is None by default
        """
        config = Configuration()
        event = self.event_class(Exception("oops"), config, {})
        payload = json.loads(event._payload())
        app = payload['events'][0]['app']

        assert app['type'] is None

    def test_configured_app_type(self):
        """
        It should include app type if specified
        """
        config = Configuration()
        config.configure(app_type='rq')
        event = self.event_class(Exception("oops"), config, {})
        payload = json.loads(event._payload())
        app = payload['events'][0]['app']

        assert app['type'] == 'rq'

    def test_default_request(self):
        config = Configuration()
        config.configure(app_type='rq')
        event = self.event_class(Exception("oops"), config, {})
        assert event.request is None

    def test_meta_data_warning(self):
        config = Configuration()
        with pytest.warns(DeprecationWarning) as records:
            event = self.event_class(Exception('oh no'), config, {},
                                     meta_data={'nuts': {'almonds': True}})

            assert len(records) > 0
            i = len(records) - 1
            assert str(records[i].message) == ('The Event "metadata" ' +
                                               'argument has been replaced ' +
                                               'with "metadata"')
            assert event.metadata['nuts']['almonds']
