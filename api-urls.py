from django.conf.urls import patterns, url

urlpatterns = patterns('objects.api',

    url(r'(?P<object_slug>[-\w]+)/$', 'object'),
    url(r'/$', 'list_objects'),

)
