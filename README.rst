nexus-memcache
--------------

Provides a memcache statistics module in `Nexus <https://github.com/dcramer/nexus>`_.

Install
=======

Install using pip, or easy_install::

	pip install nexus_memcache

Config
======

Add nexus_memcache to your ``INSTALLED_APPS``::

	INSTALLED_APPS = (
	    'nexus',
	    'nexus_memcache',
	)

Usage
=====

The memcache module is automatically integrated into Nexus and detects memcache using your ``CACHE_BACKEND`` setting.