from django.conf import settings

BACKEND = getattr(settings, 'NEXUS_MEMCACHE_BACKEND', settings.CACHE_BACKEND)
