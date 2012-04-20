from pkgutil import walk_packages


def modules_callables(module):
    return [m for m in dir(module) if callable(getattr(module, m))]


def has_doctest(docstring):
    return ">>>" in docstring


def all_doctests(module, locals_copy):
    ''' Returns list of all functions from module (including submodules),
        that have doctests.
    '''
    prefix = module.__name__ + '.'

    sub_module_names = []

    for _, modname, _ in walk_packages(path=module.__path__,
                                       prefix=prefix,
                                       onerror=lambda x: None):
        if 'doctest_finder' in modname:
            continue
        sub_module_names.append(modname)

    result = {}

    for modname in sub_module_names:
        submodule = __import__(modname, fromlist=[()])
        for method in modules_callables(submodule):
            docstring = str(getattr(submodule, method).__doc__)
            if has_doctest(docstring):
                _temp = __import__(submodule.__name__,
                                   globals(), locals(), [method])
                locals_copy[method] = getattr(_temp, method)

                result[method] = getattr(submodule, method)

    return result
