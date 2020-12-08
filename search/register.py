from collections import namedtuple
import requests

from django.apps import apps
from django.db.models.signals import post_save

from .client import client
from .errors import RegistrationError

_Options = namedtuple("Options", ("settings", "uid", "primary_key"))

_registered_models = {}


def get_registered_models():
    return (apps.get_model(*key) for key in _registered_models.keys())


def is_registered(model):
    return _get_registration_key(model) in _registered_models


def _get_registration_key(model):
    return (model._meta.app_label, model._meta.model_name)


def _get_senders_and_signals(model):
    yield model, post_save, _post_save_receiver


def _post_save_receiver(sender, instance, created, **kwargs):
    if is_registered(sender):
        add_to_search(instance, created, **kwargs)


def _assert_registered(model):
    if not is_registered(model):
        raise RegistrationError(
            "{model} has not been registered with django-meilisearch".format(
                model=model
            )
        )


def _get_options(model):
    _assert_registered(model)
    return _registered_models[_get_registration_key(model)]


def get_attribute(instance, name):
    if hasattr(instance, name):
        return getattr(instance, name)
    names = name.split("__")
    name = names.pop(0)
    if len(names) == 0:
        return None
    if hasattr(instance, name):
        value = getattr(instance, name)
        return get_attribute(value, "__".join(names))
    return None


def create_or_update_document(index, created, document):
    if created:
        return index.add_documents([document])
    else:
        return index.update_documents([document])


def create_if_needed(opts, obj, **kwargs):
    uid = opts.uid
    if callable(uid):
        uid = uid(obj)
    index = client.get_index(uid)
    try:
        create_or_update_document(index, **kwargs)
    except Exception as error:
        if error.error_code == "index_not_found":
            print(opts)
            index = client.create_index(uid, {"primaryKey": opts.primary_key})
            index.update_settings(opts.settings)
            create_or_update_document(index, **kwargs)
        else:
            raise error


def add_to_search(obj, created=False, **kwargs):
    opts = _get_options(obj.__class__)
    document = {k: get_attribute(obj, k) for k in opts.settings["displayedAttributes"]}
    create_if_needed(opts, obj, created=created, document=document)


def register(model=None, fields=[], exclude=[], distinct=None, uid=None):
    def register(model):
        searchable = [field for field in fields if field not in exclude]
        if distinct not in fields:
            raise Exception("{} missing from fields".format(distinct))
        settings = {
            "searchableAttributes": searchable,
            "displayedAttributes": fields,
            "distinctAttribute": distinct,
        }
        opts = _Options(settings=settings, uid=uid, primary_key="pk")
        _registered_models[_get_registration_key(model)] = opts
        for sender, signal, signal_receiver in _get_senders_and_signals(model):
            signal.connect(signal_receiver, sender=sender)

        return model

    # Return a class decorator if model is not given
    if model is None:
        return register
    return register(model)
