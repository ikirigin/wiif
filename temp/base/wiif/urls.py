from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'base.views.home', name='home'),
    #url(r'^blog/', include('base.urls')),

    url(r'^admin/', include(admin.site.urls)),
)
