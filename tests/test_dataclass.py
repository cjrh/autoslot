from dataclasses import dataclass
from autoslot import Slots


def test_dc():

    @dataclass
    class C():
        x: int
        y: int = 0

    print(dir(C))
    o = C(1)
    print(o)

    assert hasattr(o, '__dict__')
    assert not hasattr(o, '__slots__')

def test_dc_slots():

    @dataclass
    class C(Slots):
        x: int
        y: int = 0

    o = C(1)
    print(o)

    assert hasattr(o, '__dict__')
    assert not hasattr(o, '__slots__')
