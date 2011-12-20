from django.conf import settings

BACKEND = getattr(settings, 'NEXUS_MEMCACHE_BACKEND', getattr(settings, 'CACHE_BACKEND', None))
