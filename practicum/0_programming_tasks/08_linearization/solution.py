def linearize(object):
    if isinstance(object, (list, tuple, set, dict, range)):
        for component in object:
            for subcomponent in linearize(component):
                yield subcomponent
    elif isinstance(object, str):
        for component in object:
            yield component
    else:
        yield object
