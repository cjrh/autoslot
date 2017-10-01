.. image:: https://img.shields.io/badge/stdlib--only-yes-green.svg
    :target: https://img.shields.io/badge/stdlib--only-yes-green.svg

.. image:: https://travis-ci.org/cjrh/slots_metaclass.svg?branch=master
    :target: https://travis-ci.org/cjrh/slots_metaclass

.. image:: https://coveralls.io/repos/github/cjrh/slots_metaclass/badge.svg?branch=master
    :target: https://coveralls.io/github/cjrh/slots_metaclass?branch=master

.. image:: https://img.shields.io/pypi/pyversions/slots_metaclass.svg
    :target: https://pypi.python.org/pypi/slots_metaclass

.. image:: https://img.shields.io/github/tag/cjrh/slots_metaclass.svg
    :target: https://img.shields.io/github/tag/cjrh/slots_metaclass.svg

.. image:: https://img.shields.io/badge/install-pip%20install%20slots_metaclass-ff69b4.svg
    :target: https://img.shields.io/badge/install-pip%20install%20slots_metaclass-ff69b4.svg

.. image:: https://img.shields.io/pypi/v/slots_metaclass.svg
    :target: https://img.shields.io/pypi/v/slots_metaclass.svg

.. image:: https://img.shields.io/badge/calver-YYYY.MM.MINOR-22bfda.svg
    :target: http://calver.org/

slots_metaclass
===============

A Python metaclass to force "__slots__".

Demo
----

.. code-block:: python

   from slots_metaclass import slots

   class Compact(metaclass=slots):
       def __init__(self, a, b):
           self.x = a
           self.y = b

This produces _exactly_ the same class as if you had done:

.. code-block:: python

   from slots_metaclass import slots

   class Compact:
       __slots__ = {'x', 'y'}
       def __init__(self, a, b):
           self.x = a
           self.y = b

The benefit of using the metaclass version is that you can modify the
code inside the ``__init__()`` method to add more attributes, and those
changes will *automatically* be reflected in the ``__slots__`` definition.

How does it work?
-----------------

See for yourself--the code is embarrassingly small!

In words: the metaclass finds the ``__init__()`` method, if present, and
accesses its bytecode. It looks for all assignments to attributes of
``self``, and considers those to be desired ``__slots__`` entries. Then the
metaclass injects ``__slots__`` into the namespace of the class definition
and thereafter allows class creation to proceed as normal.

.. NOTE::
    If ``__init__`` is missing, the class will *not* have ``__slots__``
    injected. It will be a normal class with a ``__dict__`` attribute.
