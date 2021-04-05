.. image:: https://img.shields.io/badge/stdlib--only-yes-green.svg
    :target: https://img.shields.io/badge/stdlib--only-yes-green.svg

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

The benefit of using ``autoslot.Slots`` over a manual slots declaration is
that you can modify the
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
   inst.z = 123  # <-- This won't fail!

Attributes ``x`` and ``y`` will be stored in slots, while all other
dynamically-assigned attributes will go into the usual ``__dict__`` instance
inside the class.  If most of your class's attributes appear in the ``__init__()``
method (these will become slots), then the space bloat caused by dictionary
hash-table expansion will be contained to only the dynamically-assigned
attributes.

How does it work?
-----------------

See for yourself! The code is tiny.

In words: the metaclass finds the ``__init__()`` method, if present, and
accesses its bytecode. It looks for all assignments to attributes of
``self``, and considers those to be desired ``__slots__`` entries. Then the
metaclass injects ``__slots__`` into the namespace of the class definition
and thereafter allows class creation to proceed as normal.

Weakref
-------

When ``__slots__`` are used, weak references (e.g. using the weakref_
standard library module) won't work. If you need weak references, just
set it up on a new ``__slots__`` class variable as you would normally
do without using ``autoslot``:

.. code-block:: python

   from autoslot import Slots

   class Compact(Slots):
       __slots__ = ['__weakref__']

       def __init__(self, a, b):
           self.x = a
           self.y = b

Everything else will still work, and instances of ``Compact`` will now
also play nicely with the weakref_ module.

.. _weakref: https://docs.python.org/3/library/weakref.html?highlight=weakref#module-weakref
