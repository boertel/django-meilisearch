import meilisearch

from .utils import get_setting

client = meilisearch.Client(get_setting("URL"), get_setting("MASTER_KEY"))
