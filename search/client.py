import meilisearch

from django.conf import settings

client = meilisearch.Client(settings.MEILISEARCH_URL, settings.MEILISEARCH_MASTER_KEY)
