from django.core.cache import cache
from django.utils.datastructures import SortedDict

import nexus

class MemcacheModule(nexus.NexusModule):
    home_url = 'index'
    name = 'memcache'
    
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
            cache_stats = cache._cache.get_stats()
        except AttributeError:
            cache_stats = []
        
        global_stats = {
            'accepting_conns': 0,
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
        }
        for host, stats in cache_stats:
            for k in global_stats.iterkeys():
                global_stats[k] += float(stats[k])
        global_stats['total'] = len(cache_stats)

        return self.render_to_string('nexus/memcache/dashboard.html', {
            'global_stats': global_stats,
        })
    
    def index(self, request):
        try:
            cache_stats = ((k, SortedDict(sorted(v.iteritems(), key=lambda x: x[0]))) for k, v in cache._cache.get_stats())
        except AttributeError:
            cache_stats = []
        
        return self.render_to_response("nexus/memcache/index.html", {
            'cache_stats': cache_stats,
        }, request)
nexus.site.register(MemcacheModule, 'memcache', category='cache')