.. image:: https://img.shields.io/badge/stdlib--only-yes-green.svg
    :target: https://img.shields.io/badge/stdlib--only-yes-green.svg

.. image:: https://travis-ci.org/cjrh/autoslot.svg?branch=master
    :target: https://travis-ci.org/cjrh/autoslot

.. image:: https://coveralls.io/repos/github/cjrh/autoslot/badge.svg?branch=master
    :target: https://coveralls.io/github/cjrh/autoslot?branch=master

.. image:: https://img.shields.io/pypi/pyversions/autoslot.svg
    :target: https://pypi.python.org/pypi/autoslot

.. image:: https://img.shields.io/github/tag/cjrh/autoslot.svg
    :target: https://img.shields.io/github/tag/cjrh/autoslot.svg

.. image:: https://img.shields.io/badge/install-pip%20install%20autoslot-ff69b4.svg
    :target: https://img.shields.io/badge/install-pip%20install%20autoslot-ff69b4.svg

.. image:: https://img.shields.io/pypi/v/autoslot.svg
    :target: https://img.shields.io/pypi/v/autoslot.svg

.. image:: https://img.shields.io/badge/calver-YYYY.MM.MINOR-22bfda.svg
    :target: http://calver.org/

autoslot
========

Automatic "__slots__".

Demo
----

.. code-block:: python

   from autoslot import Slots

   class Compact(Slots):
       def __init__(self, a, b):
           self.x = a
           self.y = b

This produces *exactly* the same class as if you had done:

.. code-block:: python

   class Compact:
       __slots__ = {'x', 'y'}
       def __init__(self, a, b):
           self.x = a
           self.y = b

Simply: the code inside ``__init__()`` is scanned to find all assignments
to attributes on ``self``, and these are added as ``__slots__``.

The benefit of using the metaclass version is that you can modify the
code inside the ``__init__()`` method to add more attributes, and those
changes will *automatically* be reflected in the ``__slots__`` definition.

You can also have the best of both worlds: slots for fields you expect,
**as well as** a ``__dict__`` for those you don't:

.. code-block:: python

   from autoslot import SlotsPlusDict

   class SemiCompact(SlotsPlusDict):
       def __init__(self, a, b):
           self.x = a
           self.y = b

   inst = SemiCompact(1, 2)
   inst.z = 123

Attributes ``x`` and ``y`` will be stored in slots, while all other
dynamically-assigned attributes will go into the usual ``__dict__`` instance
inside the class.  If most fields are expected, then dictionary bloat will
be contained.

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
