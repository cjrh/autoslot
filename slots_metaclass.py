import dis

__all__ = ['slots']


def assignments_to_self(method):
    bc = dis.Bytecode(method)
    bcl = list(bc)
    names = []
    for this, next in zip(bcl, bcl[1:]):
        if this.argval == 'self' \
                and this.opname == 'LOAD_FAST' \
                and next.opname == 'STORE_ATTR':
            names.append(next.argval)
    return names

def slots(name, bases, ns):
    print(name, bases, ns)
    if '__init__' in ns:
        # Inject __slots__ into class namespace
        ns['__slots__'] = assignments_to_self(ns['__init__'])
    return type.__new__(type, name, bases, ns)
