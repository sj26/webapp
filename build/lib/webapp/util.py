
def isiterable(obj):
    return isinstance(obj, basestring) or getattr(obj, 'next', False) or getattr(obj, '__iter__', False) or getattr(obj, '__getitem__', False)
