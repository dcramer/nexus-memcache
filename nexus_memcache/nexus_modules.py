import socket
import warnings

from django.core.cache import get_cache, parse_backend_uri
from django.utils.datastructures import SortedDict

import nexus

from nexus_memcache import conf

def get_caches():
    caches = []
    schema, hosts, params = parse_backend_uri(conf.BACKEND)
    for host in hosts.split(';'):
        caches.append((host, get_cache('%s://%s?%s' % (schema, host, params))._cache))
    return caches
caches = get_caches()

class MemcacheModule(nexus.NexusModule):
    home_url = 'index'
    name = 'memcache'
    
    def get_stats(self, timeout=5):
        for host, cache in caches:
            default_timeout = socket.getdefaulttimeout()
            socket.setdefaulttimeout(timeout)
            try:
                stats = cache.get_stats()[0][1]
            except:
                stats = {'online': 0}
            else:
                stats['online'] = 1
            finally:
                socket.setdefaulttimeout(default_timeout)
            yield host, stats
    
    def get_title(self):
        return 'Memcache'
    
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        urlpatterns = patterns('',
            url(r'^$', self.as_view(self.index), name='index'),
        )
        
        return urlpatterns
    
    def render_on_dashboard(self, request):
        try:
            cache_stats = list(self.get_stats())
        except AttributeError:
            warnings.warn('`get_stats()` not found on cache backend')
            cache_stats = []
        
        global_stats = {
            'bytes': 0,
            'limit_maxbytes': 0,
            'curr_items': 0,
            'curr_connections': 0,
            'total_connections': 0,
            'total_items': 0,
            'cmd_get': 0,
            'get_hits': 0,
            'get_misses': 0,
            'rusage_system': 0,
            'online': 0,
        }
        for host, stats in cache_stats:
            for k in global_stats.iterkeys():
                global_stats[k] += float(stats.get(k, 0))
        global_stats['total'] = len(cache_stats)

        return self.render_to_string('nexus/memcache/dashboard.html', {
            'global_stats': global_stats,
        })
    
    def index(self, request):
        try:
            cache_stats = ((k, SortedDict(sorted(v.iteritems(), key=lambda x: x[0]))) for k, v in self.get_stats())
        except AttributeError:
            cache_stats = []
        
        return self.render_to_response("nexus/memcache/index.html", {
            'cache_stats': cache_stats,
        }, request)
nexus.site.register(MemcacheModule, 'memcache', category='cache')