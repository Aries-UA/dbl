# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, url, include

urlpatterns = patterns('',
    (r'^$', 'apps.dynModels.views.index'),
    (r'^content/$', 'apps.dynModels.views.content'),
)
