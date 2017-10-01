"""
slots_metaclass
===============

Demo:

.. code-block:: python

    from slots_metaclass import slots

    class A(metaclass=slots)
        def __init__(self):
            self.x = 1
            self.y = 2

    a = A()

The class A will be created using `__slots__`, which
means that it will not have `__dict__` and will therefore
be very space-efficient.

The novelty here is that the metaclass will _inspect the
bytecode_ of the `__init__()` method to see all attributes that
get assigned. This means that you can freely edit the
code of `__init__()`, and the metaclass will figure out
how to change the slots setting.

For this to work, you *must* use `self` as the instance identifier.

"""

__version__ = '2017.10.1'

from itertools import tee
import dis

__all__ = ['slots']


def assignments_to_self(method) -> list:
    """Given a method, collect all the attribute names for assignments
    to "self"."""
    instructions = dis.Bytecode(method)
    # The second iterable is to look ahead 1 step
    i0, i1 = tee(instructions)
    next(i1, None)
    names = set()
    for a, b in zip(i0, i1):
        accessing_self = a.argval == 'self' and a.opname == 'LOAD_FAST'
        storing_attribute = b.opname == 'STORE_ATTR'
        if accessing_self and storing_attribute:
            names.add(b.argval)
    return names

def slots(name, bases, ns):
    if '__init__' in ns:
        # Inject __slots__ into class namespace
        ns['__slots__'] = assignments_to_self(ns['__init__'])
    return type.__new__(type, name, bases, ns)
