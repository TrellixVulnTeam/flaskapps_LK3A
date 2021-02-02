Advanced usage
==============

.. highlight:: ini

`Burp-UI`_ has been written with modularity in mind. The aim is to support
`Burp`_ from the stable to the latest versions. `Burp`_ exists in two major
versions: 1.x.x and 2.x.x.

Both versions are supported by `Burp-UI`_ thanks to its modular design.
The consequence is you have various options in the configuration file to suite
everybody needs.

There are also different modules to support `Authentication`_ and `ACL`_ within
the web-interface.

.. warning::
    `Burp-UI`_ tries to be as less intrusive as possible, nevertheless it ships
    with the ability to manage `Burp`_'s configuration files.
    This feature **requires** `Burp-UI`_ to be launched on the **same** server
    that hosts your `Burp`_ instance.
    You also have to make sure the user that runs `Burp-UI`_ has **enough**
    privileges to edit those files.


Configuration
-------------

The `burpui.cfg`_ configuration file contains a ``[Global]`` section as follow:

::

    [Global]
    # burp backend to load either one of 'burp1', 'burp2', 'parallel' or 'multi'.
    # If you choose 'multi', you will have to declare at lease one 'Agent' section.
    # If you choose 'parallel', you need to configure the [Parallel] section.
    # If you choose either 'burp1' or 'burp2', you need to configure the [Burp]
    # section.
    # The [Burp] section is also used with the 'parallel' backend for the restoration
    # process.
    # You can also use whatever custom backend you like if it is located in the
    # 'plugins' directory and if it implements the right interface.
    backend = burp2
    # authentication plugin (mandatory)
    # list the misc/auth directory to see the available backends
    # to disable authentication you can set "auth = none"
    # you can also chain multiple backends. Example: "auth = ldap,basic"
    # the order will be respected unless you manually set a higher backend priority
    auth = basic
    # acl plugin (chainable, see 'auth' plugin option)
    # list misc/acl directory to see the available backends
    # default is no ACL
    acl = basic
    # audit logger plugin (chainable, see 'auth' plugin option)
    # list the misc/audit directory to see the available backends
    # default is no audit log
    audit = basic
    # list of paths to look for external plugins
    plugins = none


Each option is commented, but here is a more detailed documentation:

- *backend*: What `Burp`_ backend to load. Can either be one of *burp1*,
  *burp2*, *parallel* or *multi*, or can be whatever custom backend you like as
  long as it implements the proper interface.
  If providing a custom backend name, it must be located in the *plugins*
  directory. You can also specify a custom external module by providing the
  *dot-string* notation (example: *my.custom.backend*).

  (see `Backends`_ for more details)
- *auth*: What `Authentication`_ backend to use.
- *acl*: What `ACL`_ module to use.
- *audit*: What `Audit`_ module to use.
- *plugins*: Specify a list of paths to look for external plugins. See the
  `Plugins <plugins.html>`_ page for details on how to write plugins.


There is also a ``[UI]`` section in which you can configure some *UI*
parameters:

::

    [UI]
    # refresh interval of the pages in seconds
    refresh = 180
    # refresh interval of the live-monitoring page in seconds
    liverefresh = 5
    # list of labels to ignore (you can use regex)
    ignore_labels = "color:.*", "custom:.*"
    # format label using sed-like syntax
    format_labels = "s/^os:\s*//"
    # default strip leading path value for file restorations
    default_strip = 0


Each option is commented, but here is a more detailed documentation:

- *refresh*: Time in seconds between two refresh of the interface.
- *liverefresh*: Time in seconds between two refresh of the *live-monitor* page.
- *ignore_labels*: List of labels to ignore from parsing (regex are supported).
- *format_labels*: List of *sed-like* expressions to transform labels. Example: ``"s/^os:\s*//", "s/i/o/"`` will transform the label ``os: Windows`` into ``Wondows``.
- *default_strip*: Number of leading paths to strip by default while restoring files.

Production
----------

The `burpui.cfg`_ configuration file contains a ``[Production]`` section as
follow:

::

    [Production]
    # storage backend for session and cache
    # may be either 'default' or 'redis'
    storage = default
    # redis server to connect to
    redis = localhost:6379
    # session database to use
    # may also be a backend url like: redis://localhost:6379/0
    # if set to 'redis', the backend url defaults to:
    # redis://<redis_host>:<redis_port>/0
    # where <redis_host> is the host part, and <redis_port> is the port part of
    # the below "redis" setting
    session = default
    # cache database to use
    # may also be a backend url like: redis://localhost:6379/0
    # if set to 'redis', the backend url defaults to:
    # redis://<redis_host>:<redis_port>/1
    # where <redis_host> is the host part, and <redis_port> is the port part of
    # the below "redis" setting
    cache = default
    # whether to use celery or not
    # may also be a broker url like: redis://localhost:6379/0
    # if set to "true", the broker url defaults to:
    # redis://<redis_host>:<redis_port>/2
    # where <redis_host> is the host part, and <redis_port> is the port part of
    # the above "redis" setting
    celery = false
    # whether to rate limit the API or not
    # may also be a redis url like: redis://localhost:6379/0
    # if set to "true" or "redis" or "default", the url defaults to:
    # redis://<redis_host>:<redis_port>/3
    # where <redis_host> is the host part, and <redis_port> is the port part of
    # the above "redis" setting
    # Note: the limiter only applies to the API routes
    limiter = false
    # limiter ratio
    # see https://flask-limiter.readthedocs.io/en/stable/#ratelimit-string
    ratio = 60/minute
    # database url to store some persistent data
    # none or a connect string supported by SQLAlchemy:
    # http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls
    # example: sqlite:////var/lib/burpui/store.db
    database = none
    # you can change the prefix if you are behind a reverse-proxy under a custom
    # root path. For example: /burpui
    # You can also configure your reverse-proxy to announce the prefix through the
    # 'X-Script-Name' header. In this case, the bellow prefix will be ignored in
    # favour of the one announced by your reverse-proxy
    prefix = none
    # ProxyFix
    # number of reverse-proxy to trust in order to retrieve some HTTP headers
    # All the details can be found here:
    # https://werkzeug.palletsprojects.com/en/0.15.x/middleware/proxy_fix/#module-werkzeug.middleware.proxy_fix
    num_proxies = 0
    # alternatively, you can specify your own ProxyFix args.
    # The default is: "{'x_proto': {num_proxies}, 'x_for': {num_proxies}, 'x_host': {num_proxies}, 'x_prefix': {num_proxies}}"
    # if num_proxies > 0, else it defaults to ProxyFix defaults
    proxy_fix_args = "{'x_proto': {num_proxies}, 'x_for': {num_proxies}, 'x_host': {num_proxies}, 'x_prefix': {num_proxies}}"


- *storage*: What storage engine should be used for sessions, cache, etc. Can
  only be one of: ``default`` or ``redis``.
- *redis*: redis server to use.
- *session*: redis database to use, by default (if set to ``redis``) we use
  database **0** on the server provided in *redis*.
- *cache*: redis database to use, by default (if set to ``redis``) we use
  database **1** on the server provided in *redis*.
- *celery*: redis database to use as broker and message queue for Celery, by
  default (if set to ``true``) we use database **2** on the server provided in
  *redis*. You can also set it to ``false`` to disable Celery support.
- *limiter*: redis database to use, by default (if set to ``redis``) we use
  database **3** on the server provided in *redis*.
- *ratio*: Limiter ratio. See `Limiter <https://flask-limiter.readthedocs.io/en/stable/#ratelimit-string>`_
  documentation for details.
- *database*: Enable SQL persistent storage. Can be ``none`` (to disable SQL)
  or any valid `SQLAlchemy <http://docs.sqlalchemy.org/en/latest/core/engines.html#database-urls>`_
  connect string.
- *prefix*: You can host `Burp-UI`_ behind a sub-root path. See the `gunicorn
  <gunicorn.html#sub-root-path>`__ page for details.
- *num_proxies*: This is useful only if you host `Burp-UI`_ behind a
  `reverse-proxy <gunicorn.html#reverse-proxy>`__.
- *proxy_fix_args*: Same as above. Please refer to `Werkzeug's documentation
  <https://werkzeug.palletsprojects.com/en/0.15.x/middleware/proxy_fix/#module-werkzeug.middleware.proxy_fix>`_
  for details.


WebSocket
---------

The ``[WebSocket]`` section defines specific options for the WebSocket server.
You will find details on how to use this feature in the
`WebSocket <websocket.html>`_ page.

::

    [WebSocket]
    ## This section contains WebSocket server specific options.
    # whether to enable websocket or not
    enabled = true
    # whether to embed the websocket server or not
    # if set to "true", you should have only *one* gunicorn worker
    # see here for details:
    # https://flask-socketio.readthedocs.io/en/latest/#gunicorn-web-server
    embedded = false
    # what broker to use to interact between websocket servers
    # may be a redis url like: redis://localhost:6379/0
    # if set to "true" or "redis" or "default", the url defaults to:
    # redis://<redis_host>:<redis_port>/4
    # where <redis_host> is the host part, and <redis_port> is the port part of
    # the above "redis" setting
    # set this to none to disable the broker
    broker = redis
    # if you choose to run a dedicated websocket server (with embedded = false)
    # you can specify here the websocket url. You'll need to double quote your
    # string though.
    # example:
    # url = "document.domain + ':5001'"
    url = none
    # whether to enable verbose websocket server logs or not (for development)
    debug = false


Experimental
------------

There is a ``[Experimental]`` section for features that have not been deeply
tested:

::

    [Experimental]
    ## This section contains some experimental features that have not been deeply
    ## tested yet
    # enable zip64 feature. Python doc says:
    # « ZIP64 extensions are disabled by default because the default zip and unzip
    # commands on Unix (the InfoZIP utilities) don’t support these extensions. »
    zip64 = true


These options are also available in the `bui-agent`_ configuration file.

Security
--------

The ``[Security]`` section contains options to harden the security of the
application:

::

    [Security]
    ## This section contains some security options. Make sure you understand the
    ## security implications before changing these.
    # list of 'root' paths allowed when sourcing files in the configuration.
    # Set this to 'none' if you don't want any restrictions, keeping in mind this
    # can lead to accessing sensible files. Defaults to '/etc/burp'.
    # Note: you can have several paths separated by comas.
    # Example: /etc/burp,/etc/burp.d
    includes = /etc/burp
    # if files already included in config do not respect the above restriction, we
    # prune them
    enforce = false
    # enable certificates revocation
    revoke = false
    # remember_cookie duration in days
    cookietime = 14
    # whether to use a secure cookie for https or not. If set to false, cookies
    # won't have the 'secure' flag.
    # This setting is only useful when HTTPS is detected
    scookie = true
    # application secret to secure cookies. If you don't set anything, the default
    # value is 'random' which will generate a new secret after every restart of your
    # application. You can also set it to 'none' although this is not recommended.
    appsecret = random


Some of these options are also available in the `bui-agent`_ configuration file.


Backends
--------

`Burp-UI`_ ships with four different backends:

- `Burp1`_
- `Burp2`_
- `Multi`_
- `Parallel`_

These backends allow you to either connect to a `Burp`_ server version 1.x.x or
2.x.x.

.. note::
    If you are using a `Burp`_ server version 2.x.x you **have** to use the
    `Burp2`_ backend, no matter what `Burp`_'s protocol you are using.


Burp1
^^^^^

.. note::
    Make sure you have read and understood the `requirements
    <requirements.html#burp1>`__ first.

The *burp-1* backend can be enabled by setting the *backend* option to *burp1* in
the ``[Global]`` section of your `burpui.cfg`_ file:

::

    [Global]
    backend = burp1


Now you can refer to the `Options`_ section for further setup.


Burp2
^^^^^

.. note::
    Make sure you have read and understood the `requirements
    <requirements.html#burp2>`__ first.

.. note::
    The `gunicorn <gunicorn.html#daemon>`__ documentation may help you
    configuring your system.

The *burp-2* backend can be enabled by setting the *backend* option to *burp2* in
the ``[Global]`` section of your `burpui.cfg`_ file:

::

    [Global]
    backend = burp2


Now you can refer to the `Options`_ section for further setup.


Multi
^^^^^

The *multi* backend allows you to connect to different *bui-agents*. It can be
enabled by setting the *backend* option to *multi* in the ``[Global]`` section
of your `burpui.cfg`_ file:

::

    [Global]
    backend = multi


This backend allows you to access multiple `Burp`_ servers through the `bui-agent`_.
The architecture is available on the bui-agent
`page <buiagent.html#architecture>`__.


Once this backend is enabled, you have to create **one** ``[Agent]`` section
**per** agent you want to connect to in your `burpui.cfg`_ file:

::

    # If you set backend to 'multi', add at least one section like this per
    # bui-agent
    [Agent:agent1]
    # bui-agent address
    host = 192.168.1.1
    # bui-agent port
    port = 10000
    # bui-agent password
    password = azerty
    # enable SSL
    ssl = true

    [Agent:agent2]
    # bui-agent address
    host = 192.168.2.1
    # bui-agent port
    port = 10000
    # bui-agent password
    password = ytreza
    # enable SSL
    ssl = true


.. note:: The sections must be called ``[Agent:<label>]`` (case sensitive)

To configure your agents, please refer to the `bui-agent`_ page.


Parallel
^^^^^^^^

The *parallel* backend allows you to connect to the `bui-monitor`_ pool. It can be
enabled by setting the *backend* option to *parallel* in the ``[Global]`` section
of your `burpui.cfg`_ file:

::

    [Global]
    backend = parallel


This backend allows you to access `Burp`_ servers through the `bui-monitor`_
pool.
The architecture is available on the bui-monitor
`page <buimonitor.html#architecture>`__.


Once this backend is enabled, you have to configure the ``[Parallel]`` section.

::

    # parallel backend specific options
    [Parallel]
    # address of the monitor pool
    host = ::1
    # port of the monitor pool
    port = 11111
    # how many time to wait for the monitor pool to answer (in seconds)
    timeout = 15
    # monitor pool password
    password = password123456
    # enable SSL
    ssl = true
    # number of operations to process concurrently
    # the value should not exceed the pool size you set in the bui-monitor.cfg file
    concurrency = 2
    # time to wait at startup, mainly used by the bui-agent
    # the bui-monitor must be started before your agent, but since it needs to
    # initialize its workers first you may need to wait a bit for it to be available
    init_wait = 15


To configure your monitor pool, please refer to the `bui-monitor`_ page.


Options
^^^^^^^

::

    # burp backend specific options
    [Burp]
    # burp status address (can only be '127.0.0.1' or '::1')
    bhost = ::1
    # burp status port
    bport = 4972
    # burp binary
    burpbin = /usr/sbin/burp
    # vss_strip binary
    stripbin = /usr/sbin/vss_strip
    # burp client configuration file used for the restoration (Default: None)
    bconfcli = /etc/burp/burp.conf
    # burp server configuration file used for the setting page
    bconfsrv = /etc/burp/burp-server.conf
    # temporary directory to use for restoration
    tmpdir = /tmp
    # how many time to wait for the monitor to answer (in seconds)
    timeout = 5
    # since burp-2.1.10, timestamps have local offsets, if we detect a burp-server
    # version greater than 2.1.10 we'll suppose every backup was made with that
    # version. If this is not the case, you may end-up with wrongly computed backup
    # dates in the clients overview. For that reason, you can enable the
    # 'deep_inspection' option which will check every backup logs in order to
    # find out which server version was used.
    # The drawback is this process requires some extra work that may slow-down
    # burp-ui.
    deep_inspection = false


Each option is commented, but here is a more detailed documentation:

- *bhost*: The address of the `Burp`_ server. In burp-1.x.x, it can only be
  *127.0.0.1* or *::1*
- *bport*: The port of `Burp`_'s status port.
- *burpbin*: Path to the `Burp`_ binary (used for restorations).
- *stripbin*: Path to the `Burp`_ *vss_strip* binary (used for restorations).
- *bconfcli*: Path to the `Burp`_ client configuration file (see
  `restoration <installation.html#restoration>`__).
- *bconfsrv*: Path to the `Burp`_ server configuration file.
- *tmpdir*: Path to a temporary directory where to perform restorations.
- *timeout*: Time to wait for the monitor to answer in seconds.


Authentication
--------------

`Burp-UI`_ provides some authentication backends in order to restrict access
only to granted users.
There are currently three different backends:

- `LDAP`_
- `Basic`_
- `Local`_

To disable the *authentication* backend, set the *auth* option of the
``[Global]`` section of your `burpui.cfg`_ file to *none*:

::

    [Global]
    auth = none


You can use multiple backends, they will be sorted by priority or in the order
they are defined if no priority is found.
If a user is present in several backends, the first one that matches both login
and password will be used.

Example:

::

    [Global]
    auth = basic,ldap


LDAP
^^^^

The *ldap* authentication backend has some dependencies, please refer to the
`requirements <requirements.html#ldap>`_ page. To enable this backend, you need
to set the *auth* option of the ``[Global]`` section of your `burpui.cfg`_ file
to *ldap*:

::

    [Global]
    auth = ldap


Now you can add *ldap* specific options:

::

    # ldapauth specific options
    [LDAP:AUTH]
    # Backend priority. Higher is first
    priority = 50
    # LDAP host
    host = 127.0.0.1
    # LDAP port
    port = 389
    # Encryption type to LDAP server (none, ssl or tls)
    # - try tls if unsure, otherwise ssl on port 636
    encryption = tls
    # specifies if the server certificate must be validated, values can be:
    #  - none (certificates are ignored)
    #  - optional (not required, but validated if provided)
    #  - required (required and validated)
    validate = none
    # the file containing the certificates of the certification authorities
    cafile = none
    # Attribute to use when searching the LDAP repository
    #searchattr = sAMAccountName
    searchattr = uid
    # LDAP filter to find users in the LDAP repository
    #  - {0} will be replaced by the search attribute
    #  - {1} will be replaced by the login name
    filter = (&({0}={1})(burpui=1))
    #filter = (&({0}={1})(|(userAccountControl=512)(userAccountControl=66048)))
    # LDAP base
    base = "ou=users,dc=example,dc=com"
    # Binddn to list existing users
    binddn = "cn=admin,dc=example,dc=com"
    # Bindpw to list existing users
    bindpw = Sup3rS3cr3tPa$$w0rd


.. note:: The *host* options accepts URI style (ex: ldap://127.0.0.1:389)

.. warning:: The quotes (") around *base* and *binddn* are **MANDATORY**

Basic
^^^^^

In order for the *basic* authentication backend to be enabled, you need to set
the *auth* option of the ``[Global]`` section of your `burpui.cfg`_ file to
*basic*:

::

    [Global]
    auth = basic


Now you can add *basic* specific options:

::

    # basicauth specific options
    # Note: in case you leave this section commented, the default login/password
    # is admin/admin
    [BASIC:AUTH]
    # Backend priority. Higher is first
    priority = 100
    admin = pbkdf2:sha1:1000$12345678$password
    user1 = pbkdf2:sha1:1000$87654321$otherpassword


.. note::
    Each line defines a new user with the *key* as the username and the *value*
    as the password

.. warning::
    Since *v0.3.0*, passwords must be hashed (see `manage <manage.html#users>`_
    to know how to create new users with hashed passwords)

Local
^^^^^

In order for the *local* authentication backend to be enabled, you need to set
the *auth* option of the ``[Global]`` section of your `burpui.cfg`_ file to
*local*:

::

    [Global]
    auth = local


Now you can add *local* specific options:

::

    # localauth specific options
    # Note: if not running as root, then burp-ui must be run as group 'shadow' to
    # allow PAM to work
    [LOCAL:AUTH]
    # Backend priority. Higher is first
    priority = 0
    # List of local users allowed to login. If you don't set this setting, users
    # with uid greater than limit will be able to login
    users = user1,user2
    # Minimum uid that will be allowed to login
    limit = 1000


ACL
---

`Burp-UI`_ implements some mechanisms to restrict access on some resources only
for some users.
There is currently only one backend:

- `Basic ACL`_

To disable the *acl* backend, set the *acl* option of the ``[Global]`` section
of your `burpui.cfg`_ file to *none*:

::

    [Global]
    acl = none


The *ACL* engine has some settings as bellow:

::

    # acl engine global options
    [ACL]
    # Enable extended matching rules (enabled by default)
    # If the rule is a string like 'user1 = desk*', it will match any client that
    # matches 'desk*' no mater what agent it is attached to.
    # If it is a coma separated list of strings like 'user1 = desk*,laptop*' it
    # will match the first matching rule no mater what agent it is attached to.
    # If it is a dict like:
    # user1 = '{"agents": ["srv*", "www*"], "clients": ["desk*", "laptop*"]}'
    # It will also validate against the agent name.
    extended = true
    # If you don't explicitly specify ro/rw grants, what should we assume?
    assume_rw = true
    # The inheritance order maters, it means depending the order you choose,
    # the ACL engine won't handle the grants the same way.
    # By default, ACL inherited by groups will have lower priority, unless you
    # choose otherwise
    inverse_inheritance = false
    # If you specify agents and clients separately, should we link them implicitly?
    # For instance, '{"agents": ["agent1", "agent2"], "clients": ["client1", "client2"]}'
    # will become: '{"agents": {"agent1": ["client1", "client2"], "agent2": ["client1", "client2"]}}'
    implicit_link = true
    # Enable 'legacy' behavior
    # Since v0.6.0, if you don't specify the agents name explicitly, users will be
    # granted on every agents where a client matches user's ACL. If you enable the
    # 'legacy' behavior, you will need to specify the agents explicitly.
    # Note: enabling this option will also disable the extended mode
    legacy = false


Basic ACL
^^^^^^^^^


The *basic* acl backend can be enabled by setting the *acl* option of the
``[Global]`` section of your `burpui.cfg`_ file to *basic*:

::

    [Global]
    acl = basic


Now you can add *basic acl* specific options:

::

    # basicacl specific options
    # Note: in case you leave this section commented, the user 'admin' will have
    # access to all clients whereas other users will only see the client that have
    # the same name
    [BASIC:ACL]
    # Backend priority. Higher is first
    priority = 100
    # List of administrators
    admin = user1,user2
    # List of moderators. Users listed here will inherit the grants of the
    # group '@moderator'
    +moderator = user5,user6
    @moderator = '{"agents":{"ro":["agent1"]}}'
    # NOTE: if you are running single-agent mode, you should specify the ro/rw
    # rights of the moderators using this special 'local' agent name:
    # NOTE: this is the default when running single-agent mode if you don't
    # specify anything else
    #@moderator = '{"agents": {"rw": "local"}}'
    # Please note the double-quotes and single-quotes on the following lines are
    # mandatory!
    # You can also overwrite the default behavior by specifying which clients a
    # user can access
    # Suppose you are running single-agent mode (the default), you only need to
    # specify a list of clients a user can access:
    user3 = '{"clients": {"ro": ["prod*"], "rw": ["dev*", "test1"]}}'
    # In case you are not in a single mode, you can also specify which clients
    # a user can access on a specific Agent
    user4 = '{"agents": {"agent1": ["client6", "client7"], "agent2": ["client8"]}}'
    # You can define read-only and/or read-write grants using:
    user5 = '{"agents": {"www*": {"ro": ["desk*"], "rw": ["desk1"]}}}'
    # Finally, you can define groups using the syntax "@groupname" and adding
    # members using "+groupname". Note: groups can inherit groups!
    @group1 = '{"agents": {"ro": ["*"]}}'
    @group2 = '{"clients": {"rw": ["dev*"]}}'
    +group1 = @group2
    +group2 = user5
    # As a result, user5 will be granted the following rights:
    # '{"ro": {"agents": ["*", "agent1"], "www*": ["desk*"]}, "rw": {"clients": ["dev*"], "www*": ["desk1"]}}


.. warning:: The double-quotes and single-quotes are **MANDATORY**


By default, if a user is named ``admin`` it will be granted the admin role.
Here are the default grants:


1. *admin* => you can do anything
2. *non admin* => you can only see the client that matches your username
3. *custom* => you can manually assign username to clients using the syntax
   ``username = '{"agents": {"agent1": ["client1-1"], "agent2": ["client2-3", "client2-4"]}}'``
   (if you are running a multi-agent setup)
4. *moderators* => can edit the Burp server configurations of any agent unless
   told other wise (with ``ro`` rights), but cannot restore files unless told
   otherwise (with ``rw`` rights). Besides, moderators can create new users.
   They can also delete backups if they have ``rw`` rights on the client.


Since *v0.6.0*, you can define advanced grants through the ``rw`` and ``ro``
keyword.


- ``ro`` means you can only see backup stats and reports (this is great for
  monitoring teams/tools)
- ``rw`` means you can interact with the server in some way. For the *regular*
  users, ``rw`` means you can perform file restorations.
  For moderators, ``rw`` means you can delete backups (if burp thinks they are
  deletable), you can also create/update/delete client configuration files.


Since *v0.7.0*, you can also define an additional ``order`` keyword in order
to specify in which order the ACL engine should evaluate the rules.
The default being ``exclude``, then ``rw`` then ``ro``.
Note: any omitted value will be appended to your list (ie. ``"order": ["ro", "rw"]``
will be interpreted as ``["ro", "rw", "exclude"]``).
Example:

::

    myuser = '{"agents": {"agent1": {"order": ["ro", "rw"], "ro": ["client.specific.*"], "rw": ["client.*"]}}}'


With the above rule, the engine will treat ``client.specific.test`` as ``ro``
whereas without the ``order`` keywoard, ``client.specific.test`` would have
matched the ``rw`` rule first and thus would be considered as ``rw``.

There is also a new ``exclude`` keyword that supports excluding clients from
the matching rules. Of course, ``exclude`` also supports *globs* patterns.

Here is an example:

::

    # rule is: myuser = '{"agents": {"agent1": {"exclude": ["client.test1"], "ro": ["client.specific.*"], "rw": ["client.*", "server.*"]}, "agent2": {"rw": ["client.*"]}}}'

    In [3]: meta_grants.is_client_rw('myuser', 'client.specific.test1', 'agent1')
    Out[3]: False

    In [4]: meta_grants.is_client_rw('myuser', 'client.test1', 'agent1')
    Out[4]: False

    In [5]: meta_grants.is_client_rw('myuser', 'client.test2', 'agent1')
    Out[5]: True

    In [6]: meta_grants.is_client_rw('myuser', 'client.test1', 'agent2')
    Out[6]: True

    In [7]: meta_grants.is_client_allowed('myuser', 'client.test1', 'agent1')
    Out[7]: False

    In [8]: meta_grants.is_client_allowed('myuser', 'client.specific.test1', 'agent1')
    Out[8]: True



About the ``inverse_inheritance`` option, here is a concrete example. We assume
you have this piece of configuration:

::

    [ACL]
    inverse_inheritance = false

    [BASIC:ACL]
    example = '{"agents": {"test": {"rw": ["demo"]}}}'
    @gp_ro = '{"agents": {"*": {"ro": ["*"]}}}'
    +gp_ro = example


Then the client ``demo`` on the ``test`` agent will be granted ``rw`` rights,
anything else will be ``ro``.
Now if you set ``inverse_inheritance = true``, the ``@gp_ro`` grants will have
the highest priority, meaning the client ``demo`` on the ``test`` agent will be
granted ``ro`` rights like any other client.


Please also note the order of your rules matters (although the UI is unable to
re-order your rules).
For instance, this:

::

    [BASIC:ACL]
    user1 =
    @gp1 = '{"clients": {"rw": ["tata", "titi"]}}'
    +gp1 = user1
    @gp2 = '{"clients": {"ro": ["*"]}, "agents": {"rw": "local"}}'
    +gp2 = @gp1


Is not the same as:

::

    [BASIC:ACL]
    user1 =
    @gp2 = '{"clients": {"ro": ["*"]}, "agents": {"rw": "local"}}'
    +gp2 = @gp1
    @gp1 = '{"clients": {"rw": ["tata", "titi"]}}'
    +gp1 = user1


Audit
-----

`Burp-UI`_ implements some mechanisms to log *important* actions in a dedicated
logging target.

- `Basic Audit`_

To disable the *audit* backend, set the *audit* option of the ``[Global]``
section of your `burpui.cfg`_ file to *none*:

::

    [Global]
    audit = none

Basic Audit
^^^^^^^^^^^


The *basic* audit backend can be enabled by setting the *audit* option of the
``[Global]`` section of your `burpui.cfg`_ file to *basic*:

::

    [Global]
    audit = basic


Now you can add *basic audit* specific options:

::

    # Basic audit backend options
    [BASIC:AUDIT]
    # Backend priority. Higher is first
    priority = 100
    # debug level (CRITICAL, ERROR, WARNING, INFO, DEBUG)
    # the default is the same as your global application level
    level = WARNING
    # path to a file to log into
    logfile = none
    # maximum logfile size
    max_bytes = 30 * 1024 * 1024
    # number of files to keep
    rotate = 5


.. note::
    The *basic* audit backend inherit the global application logger, so you may
    see *duplicates* log entry depending on both your loggers debug level.


.. _Burp: http://burp.grke.org/
.. _Burp-UI: https://git.ziirish.me/ziirish/burp-ui
.. _burpui.cfg: https://git.ziirish.me/ziirish/burp-ui/blob/master/share/burpui/etc/burpui.sample.cfg
.. _bui-agent: buiagent.html
.. _bui-monitor: buimonitor.html
