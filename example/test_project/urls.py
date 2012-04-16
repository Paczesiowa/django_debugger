from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
                       url(r'^debug/', include('django_debugger.urls')),
                       url(r'^', include('test_app.urls')))
