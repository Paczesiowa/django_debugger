from django.conf.urls import patterns, url

urlpatterns = \
    patterns('',
             url(r'^view_traceback/(?P<traceback_hash>\w+)$',
                 'django_debugger.views.view_traceback',
                 name='view_traceback'),
             url(r'^eval_expr$', 'django_debugger.views.eval_expr',
                 name='eval_expr'),
             url(r'^this_always_fails$',
                 'django_debugger.views.this_always_fails'))
