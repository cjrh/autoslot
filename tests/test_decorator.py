import pytest
from autoslot import autoslot, autoslot_orig


def test_slots_orig():
    """Basic usage of the Slots metaclass."""
    @autoslot_orig
    class A:
        x = 1
        y = 2

    a = A()
    a.x = 1
    a.y = 1
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')
    assert not hasattr(a, 'a')
    assert not hasattr(a, 'b')
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    with pytest.raises(AttributeError):
        a.z = 3


def test_slots_orig2():
    """Basic usage of the Slots metaclass."""
    @autoslot_orig
    class A:
        x = 1
        y = 2

    a = A(y=3)
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')
    assert a.x == 1
    assert a.y == 3
    assert not hasattr(a, 'a')
    assert not hasattr(a, 'b')
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    with pytest.raises(AttributeError):
        a.z = 3

def test_slots():
    """Basic usage of the Slots metaclass."""
    @autoslot
    class A:
        def __init__(self, a, b):
            self.x = a
            self.y = b

    print(dir(A))
    print(A.__slots__)
    a = A(1, 2)
    a.x = 1
    a.y = 1
    assert hasattr(a, 'x')
    assert hasattr(a, 'y')
    assert not hasattr(a, 'a')
    assert not hasattr(a, 'b')
    assert hasattr(a, '__slots__')
    assert not hasattr(a, '__dict__')
    with pytest.raises(AttributeError):
        a.z = 3


