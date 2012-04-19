import sys
from re import match

from django.conf import settings
from django.test.client import RequestFactory
from django_debugger.middleware import DebuggerMiddleware
from django_debugger.tracebacks import TraceBacks
from django_webtest import WebTest


class DjangoDebuggerTest(WebTest):

    setup_auth = False

    def setUp(self):
        settings.DEBUG = True

    def test_tracebacks(self):
        tbs = TraceBacks()
        self.assertEqual(tbs.number_of_tracebacks(), 0)

        try:
            raise Exception()
        except:
            _, _, tb = sys.exc_info()

        hash_ = tbs.add_traceback(tb)
        hash2 = TraceBacks.traceback_hash(tb)
        self.assertEqual(hash_, hash2)
        self.assertEqual(tbs.number_of_tracebacks(), 1)
        self.assertEqual(type(hash_), str)
        self.assertEqual(id(tb), id(tbs.get_traceback(hash_)))
        self.assertIsNone(tbs.get_traceback('foo'))

    def test_middleware_response(self):
        response = self.app.get('/example1', status=500)
        debug_url = response.headers['X-Debug-URL']
        re_match = match('http://localhost:80/debug/view_traceback/[a-z0-9]+',
                         debug_url)
        self.assertTrue(bool(re_match))

        settings.DEBUG = False
        self.assertRaisesRegexp(Exception, 'oh noez',
                                self.app.get, '/example1')
        settings.DEBUG = True

    def test_middleware_state(self):
        request = RequestFactory().get('/example1')

        dbg_middleware = DebuggerMiddleware()

        self.assertEqual(0, dbg_middleware.state.tracebacks\
                                          .number_of_tracebacks())

        self.assertFalse(hasattr(request, 'debugger_middleware_state'))
        dbg_middleware.process_request(request)
        self.assertTrue(hasattr(request, 'debugger_middleware_state'))

        try:
            raise Exception('oh noez')
        except Exception as e:
            _, _, tb = sys.exc_info()
            dbg_middleware.process_exception(request, e)
            traceback_hash = \
                dbg_middleware.state.tracebacks.traceback_hash(tb)
            tb2 = dbg_middleware.state.tracebacks.get_traceback(traceback_hash)
            self.assertEqual(tb, tb2)
            self.assertEqual(1, dbg_middleware.state.tracebacks\
                                              .number_of_tracebacks())

    def test_inside_exceptions(self):
        self.assertRaisesRegexp(Exception, 'I failed',
                                self.app.get, '/debug/this_always_fails',
                                status=500)
