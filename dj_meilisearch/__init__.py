from .register import register
from .client import client


def query(uid, q, **kwargs):
    index = client.get_index(uid=uid)
    return index.search(q, **kwargs)
