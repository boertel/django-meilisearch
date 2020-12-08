import django.conf import settings


def get_setting(name, default=None):
    try:
        return getattr(settings, 'MEILISEARCH_{}'.format(name))
    except AttributeError:
        return default
