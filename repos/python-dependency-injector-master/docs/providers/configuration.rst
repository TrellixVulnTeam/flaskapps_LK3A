.. _configuration-provider:

Configuration provider
======================

.. meta::
   :keywords: Python,DI,Dependency injection,IoC,Inversion of Control,Configuration,Injection,
              Option,Ini,Json,Yaml,Dict,Environment Variable,Load,Read,Get
   :description: Configuration provides configuration options to the other providers. This page
                 demonstrates how to use Configuration provider to inject the dependencies, load
                 a configuration from an ini or yaml file, dictionary or an environment variable.

.. currentmodule:: dependency_injector.providers

:py:class:`Configuration` provider provides configuration options to the other providers.

.. literalinclude:: ../../examples/providers/configuration/configuration.py
   :language: python
   :emphasize-lines: 7,12-13
   :lines: 3-

It implements the principle "use first, define later".

.. contents::
   :local:
   :backlinks: none

Loading from an INI file
------------------------

``Configuration`` provider can load configuration from an ``ini`` file using the
:py:meth:`Configuration.from_ini` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_ini.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12

where ``examples/providers/configuration/config.ini`` is:

.. literalinclude:: ../../examples/providers/configuration/config.ini
   :language: ini

:py:meth:`Configuration.from_ini` method supports environment variables interpolation. Use
``${ENV_NAME}`` format in the configuration file to substitute value of the environment
variable ``ENV_NAME``.

Loading from a YAML file
------------------------

``Configuration`` provider can load configuration from a ``yaml`` file using the
:py:meth:`Configuration.from_yaml` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_yaml.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12

where ``examples/providers/configuration/config.yml`` is:

.. literalinclude:: ../../examples/providers/configuration/config.yml
   :language: ini

:py:meth:`Configuration.from_yaml` method uses custom version of ``yaml.SafeLoader``.

The loader supports environment variables interpolation. Use ``${ENV_NAME}`` format
in the configuration file to substitute value of the environment variable ``ENV_NAME``.

You can also specify a YAML loader as an argument:

.. code-block:: python

   import yaml


   container.config.from_yaml('config.yml', loader=yaml.UnsafeLoader)

.. note::

   Loading of a yaml configuration requires ``PyYAML`` package.

   You can install the ``Dependency Injector`` with an extra dependency::

      pip install dependency-injector[yaml]

   or install ``PyYAML`` directly::

      pip install pyyaml

   *Don't forget to mirror the changes in the requirements file.*

Loading from a dictionary
-------------------------

``Configuration`` provider can load configuration from a Python ``dict`` using the
:py:meth:`Configuration.from_dict` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_dict.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12-19

Loading from an environment variable
------------------------------------

``Configuration`` provider can load configuration from an environment variable using the
:py:meth:`Configuration.from_env` method:

.. literalinclude:: ../../examples/providers/configuration/configuration_env.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18-20

Loading from the multiple sources
---------------------------------

``Configuration`` provider can load configuration from the multiple sources. Loaded
configuration is merged recursively over the existing configuration.

.. literalinclude:: ../../examples/providers/configuration/configuration_multiple.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12-13

where ``examples/providers/configuration/config.local.yml`` is:

.. literalinclude:: ../../examples/providers/configuration/config.local.yml
   :language: ini

Mandatory and optional sources
------------------------------

By default, methods ``.from_yaml()`` and ``.from_ini()`` ignore errors if configuration file does not exist.
You can use this to specify optional configuration files.

If configuration file is mandatory, use ``required`` argument. Configuration provider will raise an error
if required file does not exist.

You can also use ``required`` argument when loading configuration from dictionaries and environment variables.

Mandatory YAML file:

.. code-block:: python

   container.config.from_yaml('config.yaml', required=True)

Mandatory INI file:

.. code-block:: python

   container.config.from_ini('config.ini', required=True)

Mandatory dictionary:

.. code-block:: python

   container.config.from_dict(config_dict, required=True)

Mandatory environment variable:

.. code-block:: python

   container.config.api_key.from_env('API_KEY', required=True)

See also: :ref:`configuration-strict-mode`.

Specifying the value type
-------------------------

You can specify the type of the injected configuration value explicitly.

This helps when you read the value from an ini file or an environment variable and need to
convert it into an ``int`` or a ``float``.

.. literalinclude:: ../../examples/providers/configuration/configuration_type.py
   :language: python
   :lines: 3-
   :emphasize-lines: 19

``Configuration`` provider has next helper methods:

- ``.as_int()``
- ``.as_float()``
- ``.as_(callback, *args, **kwargs)``

The last method ``.as_(callback, *args, **kwargs)`` helps to implement other conversions.

.. literalinclude:: ../../examples/providers/configuration/configuration_type_custom.py
   :language: python
   :lines: 3-
   :emphasize-lines: 18

With the ``.as_(callback, *args, **kwargs)`` you can specify a function that will be called
before the injection. The value from the config will be passed as a first argument. The returned
value will be injected. Parameters ``*args`` and ``**kwargs`` are handled as any other injections.

.. _configuration-strict-mode:

Strict mode and required options
--------------------------------

You can use configuration provider in strict mode. In strict mode configuration provider raises an error
on access to any undefined option.

.. literalinclude:: ../../examples/providers/configuration/configuration_strict.py
   :language: python
   :lines: 3-
   :emphasize-lines: 12

Methods ``.from_*()`` in strict mode raise an exception if configuration file does not exist or
configuration data is undefined:

.. code-block:: python
   :emphasize-lines: 10,15,20,25

   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(strict=True)


   if __name__ == '__main__':
       container = Container()

       try:
           container.config.from_yaml('does-not_exist.yml')  # raise exception
       except FileNotFoundError:
           ...

       try:
           container.config.from_ini('does-not_exist.ini')  # raise exception
       except FileNotFoundError:
           ...

       try:
           container.config.from_env('UNDEFINED_ENV_VAR')  # raise exception
       except ValueError:
           ...

       try:
           container.config.from_dict({})  # raise exception
       except ValueError:
           ...

You can override ``.from_*()`` methods behaviour in strict mode using ``required`` argument:

.. code-block:: python

   class Container(containers.DeclarativeContainer):

       config = providers.Configuration(strict=True)


   if __name__ == '__main__':
       container = Container()

       container.config.from_yaml('config.yml')
       container.config.from_yaml('config.local.yml', required=False)

You can also use ``.required()`` option modifier when making an injection. It does not require to switch
configuration provider to strict mode.

.. literalinclude:: ../../examples/providers/configuration/configuration_required.py
   :language: python
   :lines: 11-20
   :emphasize-lines: 8-9

.. note::

   Modifier ``.required()`` should be specified before type modifier ``.as_*()``.

Injecting invariants
--------------------

You can inject invariant configuration options based on the value of the other configuration
option.

To use that you should provide the switch-value as an item of the configuration option that
contains sections ``config.options[config.switch]``:

- When the value of the ``config.switch`` is ``A``, the ``config.options.A`` is injected
- When the value of the ``config.switch`` is ``B``, the ``config.options.B`` is injected

.. literalinclude:: ../../examples/providers/configuration/configuration_itemselector.py
   :language: python
   :lines: 3-
   :emphasize-lines: 15,30-31,38

.. disqus::
