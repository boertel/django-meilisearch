from .register import register
from .client import client

__version__ = '0.1.3'

VERSION = __version__

def query(uid, q, **kwargs):
    index = client.get_index(uid=uid)
    return index.search(q, **kwargs)
