Plugins
=======

Since *v0.6.0*, you can write your own external plugins.
For now, *authentication*,  *acl* and *audit* plugins are supported.

Authentication
--------------

You will find here a fully working example of an external *authentication*
plugin.
Please refer to the `Auth API <auth.html>`_ page for more details.

.. code-block:: python
    :linenos:

    from burpui.misc.auth import interface

    __type__ = 'auth'

    class UserHandler(interface.BUIhandler):
        name = 'CUSTOM:AUTH'
        priority = 1000

        def __init__(self, app):
            self.users = {
                'toto': CustomUser('toto', 'toto'),
                'tata': CustomUser('tata', 'tata'),
                'titi': CustomUser('titi', 'titi'),
                'tutu': CustomUser('tutu', 'tutu'),
            }

        def user(self, name):
            return self.users.get(name, None)

        @property
        def loader(self):
            return self

    class CustomUser(interface.BUIuser):
        def __init__(self, name, password):
            self.name = self.id = name
            self.password = password

        def login(self, passwd):
            self.authenticated = passwd == self.password
            return self.authenticated


Line 1 is mandatory since you must implement the *auth* interface in order for
your plugin to work.

Line 3 ``__type__ = 'auth'`` defines a *auth* plugin.

Line 6 defines your *auth* backend name.

The rest of the code is just a minimal implementation of the *auth* interface.

This plugin defines four hardcoded users: *toto*, *tata*, *titi*, *tutu* with
respectively the same passwords as their username.

You can put this code in a file called *custom.py*, save this file in
*/etc/burp/plugins* for instance, and set ``plugins = /etc/burp/plugins``.
The plugin will be automatically loaded.

.. note:: This is just an example, do not run this particular plugin in production!

ACL
---

You will find here a fully working example of an external *acl* plugin.
Please refer to the `ACL API <acl.html>`_ page for more details.

.. code-block:: python
    :linenos:

        from burpui.misc.acl import interface

        __type__ = 'acl'

        class ACLloader(interface.BUIaclLoader):
            name = 'CUSTOM:ACL'
            priority = 1000

            def __init__(self, app):
                self.app = app
                self.admin = 'toto'
                self._acl = CustomACL(self)

            @property
            def acl(self):
                return self._acl

            @property
            def grants(self):
                return None

            @property
            def groups(self):
                return None

            def reload(self):
                """This method is used to reload the rules in case of config
                change for instance"""
                pass


        class CustomACL(interface.BUIacl):

            def __init__(self, loader):
                self.loader = loader

            def is_admin(self, username=None):
                if not username:
                    return False
                return username == self.loader.admin

            def is_moderator(self, username=None):
                if not username:
                    return False
                return username == self.loader.admin

            def is_client_rw(self, username=None, client=None, server=None):
                if not username:
                    return False
                return username == self.loader.admin

            def is_client_allowed(self, username=None, client=None, server=None):
                if not username:
                    return False
                return username == self.loader.admin

            def is_server_rw(self, username=None, server=None):
                if not username:
                    return False
                return username == self.loader.admin

            def is_server_allowed(self, username=None, server=None):
                if not username:
                    return False
                return username == self.loader.admin


Line 1 is mandatory since you must implement the *acl* interface in order for
your plugin to work.

Line 3 ``__type__ = 'acl'`` defines a *acl* plugin.

Line 6 defines your *acl* backend name.

The rest of the code is just a minimal implementation of the *acl* interface.

This plugin defines a hardcoded admin user: *toto* which will be granted admin
rights through the whole application.

You can put this code in a file called *custom_acl.py*, save this file in
*/etc/burp/plugins* for instance, and set ``plugins = /etc/burp/plugins``.
The plugin will be automatically loaded.

.. note:: This is just an example, do not run this particular plugin in production!


ACL engine has built-in ``Groups`` support, to take full advantage of this
feature, it is recommended to use the ``meta_grants`` object as shown bellow:

.. note:: The grant syntax is explained in the `ACL <advanced_usage.html#acl>`__ documentation

.. code-block:: python
    :linenos:

        from burpui.misc.acl.meta import meta_grants
        from burpui.misc.acl import interface

        from six import iteritems

        __type__ = 'acl'

        class ACLloader(interface.BUIaclLoader):
            name = 'CUSTOM2:ACL'
            priority = 1001

            _groups = {
                'gp1': {
                    'grants': '["server1", "server2"]',  # this needs to be a string
                    'members': ['user1'],
                },
            }

            def __init__(self, app):
                self.app = app
                self.admin = 'toto'
                self.init_rules()
                self._acl = meta_grants
                # We need to register our backend in order to be notified of
                # configuration changes in other registered backends.
                # This will then call our 'reload' function in order to re-apply
                # our grants.
                meta_grants.register_backend(self.name, self)

            def init_rules(self):
                for gname, content in iteritems(self._groups):
                    meta_grants.set_group(gname, content['members'])
                    meta_grants.set_grant(gname, content['grants'])

            @property
            def acl(self):
                return self._acl

            @property
            def grants(self):
                return self.acl.grants

            @property
            def groups(self):
                return self._groups

            def reload(self):
                """This method is used to reload the rules in case of config
                change for instance"""
                self.init_rules()


You can omit either the ``meta_grants.set_grant`` or the
``meta_grants.set_group`` part if you like. For instance to define the grants
of a given group using another ACL backend, and using your plugin to manage
groups membership only.

Audit
-----

# BUIaudit, BUIauditLogger as BUIauditLoggerInterface
You will find here a fully working example of an external *audit* plugin.
Please refer to the `Audit API <audit.html>`_ page for more details.

.. code-block:: python
    :linenos:

    from burpui.misc.audit import interface

    import logging

    __type__ = 'audit'

    class BUIauditLoader(interface.BUIhandler):
        name = 'CUSTOM:AUDIT'
        priority = 1000

        def __init__(self, app):
            self.app = app
            self.conf = app.conf
            self.level = default = logging.getLevelName(self.app.logger.getEffectiveLevel())

            if self.section in self.conf.options:
                self.level = self.conf.safe_get(
                    'level',
                    section=self.section,
                    defaults=default
                )

            if self.level != default:
                self.level = logging.getLevelName(f'{self.level}'.upper())
                if not isinstance(self.level, int):
                    self.level = default

            self._logger = BUIauditLogger(self)


    class BUIauditLogger(interface.BUIauditLogger):

        def __init__(self, loader):
            self.loader = loader
            self._level = self.loader.level

            self.LOG_FORMAT = 'CUSTOM AUDIT LOG %(levelname)s in %(from)s: %(message)s'

        def log(self, level, message, *args, **kwargs):
            kwargs['levelname'] = level
            kwargs['message'] = message % args if args else message
            print(self.LOG_FORMAT % kwargs)


Line 1 is mandatory since you must implement the *audit* interface in order for
your plugin to work.

Line 5 ``__type__ = 'audit'`` defines a *auth* plugin.

Line 8 defines your *auth* backend name.

The rest of the code is just a minimal implementation of the *audit* interface.

You **must** define a ``self._logger`` object that implements the
``BUIauditLogger`` interface (see line 28).


In our example, the ``BUIauditLogger`` object is defined line 31.

This object **must** implement the ``log`` method. This is the method that will
be called when the *loglevel* matches your minimal log level.
