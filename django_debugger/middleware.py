import inspect
import sys

from django.conf import settings
from django_debugger.tracebacks import TraceBacks
from django_debugger.views import view_traceback


def is_internal_exception(traceback):
    ''' Returns True if current exception traceback was thrown from inside
        django_debugger application.
    '''
    frames = inspect.getinnerframes(traceback)
    for frame in frames:
        filename = frame[1]
        if filename.endswith('/django_debugger/views.py'):
            return True
    return False


class DebuggerMiddlewareState(object):
    ''' Simple object with debugger middleware state
        There is only one instance of middleware object per
        django app run, so this state object is shared
        for all requests.
    '''

    def __init__(self):
        self.tracebacks = TraceBacks()


class DebuggerMiddleware(object):
    ''' Middleware that displays exceptions with integrated debugger.
    '''

    def __init__(self):
        self.state = DebuggerMiddlewareState()

    def process_request(self, request):
        ''' Attach middleware state to requests,
            debugger views need tracebacks to handle code evaluation.
        '''
        if settings.DEBUG != True:
            return None
        request.debugger_middleware_state = self.state

    def process_exception(self, request, exception):
        ''' Stores exception traceback in middleware state,
            and displays traceback view.
        '''
        if settings.DEBUG != True:
            return None

        _, _, tb = sys.exc_info()

        if is_internal_exception(tb):
            return None

        traceback_hash = self.state.tracebacks.add_traceback(tb)
        return view_traceback(request, traceback_hash)
