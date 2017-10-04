"""
autoslot
========

Demo:

.. code-block:: python

    from autoslot import Slots

    class A(Slots)
        def __init__(self):
            self.x = 1
            self.y = 2

    a = A()

The class A will be created using ``__slots__``, which
means that it will not have ``__dict__`` and will therefore
be very space-efficient.

The novelty here is that the metaclass will _inspect the
bytecode_ of the ``__init__()`` method to see all attributes that
get assigned. This means that you can freely edit the
code of ``__init__()``, and the metaclass will figure out
how to change the slots setting.

"""

from itertools import tee
import dis

__version__ = '2017.10.3'
__all__ = ['Slots', 'SlotsMeta', 'SlotsPlusDict', 'SlotsPlusDictMeta']


def assignments_to_self(method) -> list:
    """Given a method, collect all the attribute names for assignments
    to "self"."""
    # Get the name of the var used to refer to the instance. Usually,
    # this will be "self". It's the first parameter to the
    # __init__(self, ...)  method call. If there are no parameters,
    # just pretend it was "self".
    instance_var = next(iter(method.__code__.co_varnames), 'self')
    # We need to scan all the bytecode instructions to see all the times
    # an attribute of "self" got assigned-to. First get the list of
    # instructions.
    instructions = dis.Bytecode(method)
    # Assignments to attributes of "self" are identified by a first
    # LOAD_FAST (with a value of "self") immediately followed by a
    # STORE_ATTR (with a value of the attribute name). So we will need
    # to look at a sequence of pairs through the bytecode. The easiest
    # way to do this is with two iterators.
    i0, i1 = tee(instructions)
    # March the second one ahead by one step.
    next(i1, None)
    names = set()
    # a and b are a pair of instructions; b follows a.
    for a, b in zip(i0, i1):
        accessing_self = (a.argval == instance_var and a.opname == 'LOAD_FAST')
        storing_attribute = (b.opname == 'STORE_ATTR')
        if accessing_self and storing_attribute:
            names.add(b.argval)
    return names


class SlotsMeta(type):
    def __new__(mcs, name, bases, ns):
        # Caller may have already provided slots, in which case just
        # retain them and keep going.
        slots = set(ns.get('__slots__', ()))
        if '__init__' in ns:
            slots |= assignments_to_self(ns['__init__'])
        ns['__slots__'] = slots
        return super().__new__(mcs, name, bases, ns)

class Slots(metaclass=SlotsMeta):
    pass

class SlotsPlusDictMeta(SlotsMeta):
    def __new__(mcs, name, bases, ns):
        # slots = set(ns.get('__slots__', ()))
        slots = set(ns.get('__slots__', ()))
        if '__init__' in ns:
            slots.add('__dict__')
        ns['__slots__'] = slots
        return super().__new__(mcs, name, bases, ns)

class SlotsPlusDict(metaclass=SlotsPlusDictMeta):
    pass
