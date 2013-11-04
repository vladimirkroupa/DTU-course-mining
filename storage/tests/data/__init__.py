import os
from storage.tests import __file__ as test_directory

def data_dir():
    return os.path.join(os.path.dirname(test_directory), 'data')