import os

def sqlite_uri_for_file(fn):
    return 'sqlite:///' + os.path.abspath(fn)
#-- sqlite_uri_for_file
