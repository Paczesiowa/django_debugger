from django.conf.urls import patterns, url

urlpatterns = \
    patterns('', url(r'^view_traceback/(?P<traceback_hash>\w+)$',
                     'django_debugger.views.view_traceback',
                     name='view_traceback'))
