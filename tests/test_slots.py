import pytest
from slots_metaclass import slots

def test_normal():
    class A():
        def __init__(self, a, b):
            self.x = a
            self.y = b

    a = A(1, 2)
    assert hasattr(a, 'x')
    assert hasattr(a, '__dict__')
    assert not hasattr(a, '__slots__')
    a.z = 3
    assert hasattr(a, 'z')


def test_slots():
    class A(metaclass=slots):
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
    assert not hasattr(a, 'a')
    assert not hasattr(a, 'b')
    assert not hasattr(a, 'z')
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    with pytest.raises(AttributeError):
        a.z = 3

def test_no_init():
    class A(metaclass=slots):
        pass

    a = A()
    assert not hasattr(a, '__slots__')
    assert hasattr(a, '__dict__')
