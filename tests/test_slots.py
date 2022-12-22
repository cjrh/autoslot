import pytest
from autoslot import Slots, SlotsPlusDict


def test_normal():
    """This is just normal behaviour: nothing different."""
    class A:
        def __init__(self, a, b):
            self.x = a
            self.y = b

    a = A(1, 2)
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')
    assert hasattr(a, '__dict__')
    assert not hasattr(a, '__slots__')
    a.z = 3
    assert hasattr(a, 'z')


def test_slots():
    """Basic usage of the Slots metaclass."""
    class A(Slots):
        def __init__(self, a, b):
            self.x = a
            self.y = b
            # Testing to see that the
            # bytecode processor identifies things
            # correctly.
            self.x = 'bleh'

    assert '__module__' in A.__dict__
    assert '__init__' in A.__dict__
    assert '__slots__' in A.__dict__
    assert A.__dict__['__slots__'] == {'x', 'y'}

    a = A(1, 2)
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')
    # Just checking that we didn't pick up the wrong names
    assert not hasattr(a, 'a')
    assert not hasattr(a, 'b')
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    # Can't assign new attributes
    with pytest.raises(AttributeError):
        a.z = 3


def test_slots_load_deref():
    """Values can come from either LOAD_FAST or LOAD_DEREF
    opcodes, so we need to handle both."""
    class A(Slots):
        def __init__(self, a, b):
            self.x = a

            def f():
                """Simply by referring to self in another scope
                is enough to change the `self` accessing opcodes
                in __init__ to become LOAD_DEREF instead of
                LOAD_FAST. We don't even have to call `f`."""
                print(self)

            self.y = b

            # Testing to see that the
            # bytecode processor identifies things
            # correctly.
            self.x = 'bleh'

    assert '__module__' in A.__dict__
    assert '__init__' in A.__dict__
    assert '__slots__' in A.__dict__
    assert A.__dict__['__slots__'] == {'x', 'y'}

    a = A(1, 2)
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')
    # Just checking that we didn't pick up the wrong names
    assert not hasattr(a, 'a')
    assert not hasattr(a, 'b')
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    # Can't assign new attributes
    with pytest.raises(AttributeError):
        a.z = 3


def test_slots_weakref():
    """Basic usage of the Slots metaclass."""
    class A(Slots):
        __slots__ = ['__weakref__']

        def __init__(self, a, b):
            self.x = a
            self.y = b
            # Testing to see that the
            # bytecode processor identifies things
            # correctly.
            self.x = 'bleh'

    assert '__module__' in A.__dict__
    assert '__init__' in A.__dict__
    assert '__slots__' in A.__dict__
    assert A.__dict__['__slots__'] == {'__weakref__', 'x', 'y'}

    a = A(1, 2)
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')
    # Just checking that we didn't pick up the wrong names
    assert not hasattr(a, 'a')
    assert not hasattr(a, 'b')
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    # Can't assign new attributes
    with pytest.raises(AttributeError):
        a.z = 3

    import weakref
    r = weakref.ref(a)
    assert r


def test_no_init():
    class A(Slots):
        pass

    a = A()
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')


def test_conditional():
    """What happens if you conditionally create attributes inside
    __init__()?"""
    class A(Slots):
        def __init__(self, a):
            if a == 0:
                self.x = 1
            elif a == 1:
                self.y = 1

    # "if" is hit
    a = A(0)
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    # Both attributes will get slots.
    assert {'x', 'y'} < set(dir(a))

    # "elif" is hit
    a = A(1)
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    # Both attributes will get slots.
    assert {'x', 'y'} < set(dir(a))

    # Neither branch hit
    a = A(2)
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    # Both attributes will get slots.
    assert {'x', 'y'} < set(dir(a))


def test_inherit_new():
    """Normal inheritance will propagate the metaclass. Note that
    you MUST call super().__init__() if you want slots for the parents
    to be created."""
    class A(Slots):
        def __init__(self, a, b):
            self.x = a
            self.y = b

    class B(A):
        def __init__(self, c, d):
            super().__init__(1, 2)
            self.w = c
            self.z = d

    class C(B):
        """Missing call to superclass initializer."""
        def __init__(self, e, f):
            self.ww = e
            self.zz = f

    a = A(1, 2)
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')

    # Instances of B have slots from A in addition to their own.
    b = B(3, 4)
    assert hasattr(b, 'x')
    assert hasattr(b, 'y')
    assert hasattr(b, 'w')
    assert hasattr(b, 'z')
    assert hasattr(b, '__slots__')
    assert not hasattr(b, '__dict__')

    c = C(5, 6)
    assert hasattr(c, '__slots__')
    assert not hasattr(c, '__dict__')
    assert not hasattr(c, 'x')
    assert not hasattr(c, 'y')
    assert not hasattr(c, 'w')
    assert not hasattr(c, 'z')
    assert hasattr(c, 'ww')
    assert hasattr(c, 'zz')

    with pytest.raises(AttributeError):
        c.www = 123


def test_wrong_instance_var():
    """Also works if you don't use 'self' as the instance var name"""
    class A(Slots):
        def __init__(blah, a, b):
            blah.x = a
            blah.y = b

    a = A(1, 2)
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')
    # Just checking that we didn't pick up the wrong things in
    # slots_metaclass.assignments_to_self.
    assert not hasattr(a, 'a')
    assert not hasattr(a, 'b')
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    # Can't assign new attributes
    with pytest.raises(AttributeError):
        a.z = 3


def test_slots_plus_dict():
    """You can also have both: slots for some vars, and dynamic assignment
    for other vars."""
    class A(SlotsPlusDict):
        def __init__(self, a, b):
            self.x = a
            self.y = b

    a = A(1, 2)
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')
    # Just checking that we didn't pick up the wrong things in
    # slots_metaclass.assignments_to_self.
    assert not hasattr(a, 'a')
    assert not hasattr(a, 'b')
    assert hasattr(a, '__slots__')
    assert hasattr(a, '__dict__')
    # This now succeeds because there is a __dict__
    a.z = 3

    assert {'x', 'y'} < set(dir(a))
    # Note that x and y ARE NOT in the dict. This is where the space
    # savings come from.
    assert dict(z=3) == a.__dict__


def test_slots_plus_dict_empty():
    """You will always have to pay the cost of having an empty dict
    laying around though."""
    class A(SlotsPlusDict):
        def __init__(self, a, b):
            self.x = a
            self.y = b

    a = A(1, 2)
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')
    # Just checking that we didn't pick up the wrong things in
    # slots_metaclass.assignments_to_self.
    assert not hasattr(a, 'a')
    assert not hasattr(a, 'b')
    assert hasattr(a, '__slots__')
    assert hasattr(a, '__dict__')

    assert {'x', 'y'} < set(dir(a))
    # Doesn't lazy-initialize, unfortunately.
    assert {} == a.__dict__


def test_slots_existing():
    """You can also provide your own slots if you like"""
    class A(Slots):
        __slots__ = ('z',)

        def __init__(self, a, b):
            self.x = a
            self.y = b

    a = A(1, 2)
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    assert {'x', 'y', 'z'} == a.__slots__
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')

    # The instance does not have an attribute until you assign it.
    assert not hasattr(a, 'z')
    with pytest.raises(AttributeError):
        a.z

    # Assign to it, then hasattr will fail
    a.z = 123
    assert hasattr(a, 'z')

    with pytest.raises(AttributeError):
        a.totallynew = 456


def test_slots_existing_with_dict():
    """You can also provide your own slots if you like"""
    class A(SlotsPlusDict):
        __slots__ = {'z'}

        def __init__(self, a, b):
            self.x = a
            self.y = b

    a = A(1, 2)
    assert hasattr(a, '__slots__')
    assert hasattr(a, '__dict__')
    # NOTE! even though __dict__ was injected internally into the
    # slots array of the class, in the INSTANCE, __dict__ no longer
    # appears.
    assert {'x', 'y', 'z'} == a.__slots__
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')

    assert not hasattr(a, 'z')
    with pytest.raises(AttributeError):
        a.z

    a.z = 123
    assert hasattr(a, 'z')

    a.totallynew = 456
    assert a.totallynew == 456


def test_much_inherit():
    """Very long inheritance chain."""
    class A(Slots):
        def __init__(self):
            self.x = 1

    class B(A):
        def __init__(self):
            super().__init__()
            self.y = 2

    class C(B):
        def __init__(self):
            super().__init__()
            self.z = 3

    class D(C):
        def __init__(self):
            super().__init__()
            self.u = 4

    class E(D):
        def __init__(self):
            super().__init__()
            self.v = 5

    e = E()
    assert hasattr(e, '__slots__')
    assert not hasattr(e, '__dict__')
    assert all(hasattr(e, attr) for attr in 'x y z u v'.split())

    with pytest.raises(AttributeError):
        e.w = 123


def test_much_inherit_dict():
    """Very long inheritance chain."""
    class A(SlotsPlusDict):
        def __init__(self):
            self.x = 1

    class B(A):
        def __init__(self):
            super().__init__()
            self.y = 2

    class C(B):
        def __init__(self):
            super().__init__()
            self.z = 3

    class D(C):
        def __init__(self):
            super().__init__()
            self.u = 4

    class E(D):
        def __init__(self):
            super().__init__()
            self.v = 5

    e = E()
    assert hasattr(e, '__slots__')
    assert hasattr(e, '__dict__')
    assert all(hasattr(e, attr) for attr in 'x y z u v'.split())

    e.w = 123
