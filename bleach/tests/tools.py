

def in_(l, a, msg=None):
    """Shorthand for 'assert a in l, "%r not in %r" % (a, l)
    """
    if a not in l:
        raise AssertionError(msg or "%r not in %r" % (a, l))
