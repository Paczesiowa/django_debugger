from django.shortcuts import render
from django.core.urlresolvers import reverse


def view_traceback(request, traceback_hash):
    ctx = {'traceback_hash': traceback_hash}
    response = render(request, 'django_debugger/view_traceback.html',
                      ctx, status=500)
    self_url_path = reverse('view_traceback', kwargs={'traceback_hash':
                                                          traceback_hash})
    self_url = request.build_absolute_uri(self_url_path)
    response['X-Debug-URL'] = self_url
    return response
