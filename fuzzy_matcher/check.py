def myfunc(a, b, *args, **kwargs):
    c = kwargs.get('c', None)
    d = kwargs.get('d', None)


myfunc(1, 2, c='nick', d='dog')