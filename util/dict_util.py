__author__ = 'prasopes'

def tuple_to_dict(keys, tuple):
    if len(keys) != len(tuple):
        raise ValueError('Lengths do not match. {} != {}'.format(len(keys), len(tuple)))
    result = {}
    for key, value in zip(keys, tuple):
        result[key] = value
    return result