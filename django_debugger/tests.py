import sys
import urllib
from re import match

import django_debugger
import django_debugger.utils as utils
from django.conf import settings
from django.test import LiveServerTestCase
from django.test.client import RequestFactory
from django_debugger.doctest_finder import all_doctests
from django_debugger.middleware import DebuggerMiddleware
from django_debugger.tracebacks import TraceBacks
from django_webtest import WebTest
from pyvirtualdisplay import Display
from selenium.webdriver.firefox.webdriver import WebDriver


__test__ = all_doctests(django_debugger, locals())


class DjangoDebuggerTest(WebTest):

    setup_auth = False

    def setUp(self):
        settings.DEBUG = True

    def test_tracebacks(self):
        tbs = TraceBacks()
        self.assertEqual(tbs.number_of_tracebacks(), 0)

        exc = Exception()
        try:
            raise exc
        except:
            _, _, tb = sys.exc_info()

        hash_ = tbs.add_traceback(tb, exc)
        hash2 = TraceBacks.traceback_hash(tb)
        self.assertEqual(hash_, hash2)
        self.assertEqual(tbs.number_of_tracebacks(), 1)
        self.assertEqual(type(hash_), str)
        self.assertEqual(id(tb), id(tbs.get_traceback(hash_)[0]))
        self.assertEqual(id(exc), id(tbs.get_traceback(hash_)[1]))
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
            tb2, exc2 = \
                dbg_middleware.state.tracebacks.get_traceback(traceback_hash)
            self.assertEqual(tb, tb2)
            self.assertEqual(e, exc2)
            self.assertEqual(1, dbg_middleware.state.tracebacks\
                                              .number_of_tracebacks())

    def test_inside_exceptions(self):
        self.assertRaisesRegexp(Exception, 'I failed',
                                self.app.get, '/debug/this_always_fails',
                                status=500)

    def _eval_expr_url(self, traceback_hash=None, expr=None,
                       frame_number=None):
        path = '/debug/eval_expr'
        query_args = {}
        if traceback_hash is not None:
            query_args['traceback_hash'] = traceback_hash
        if frame_number is not None:
            query_args['frame_number'] = str(frame_number)
        if expr is not None:
            query_args['expr'] = expr
        query_string = urllib.urlencode(query_args)
        result = path
        if query_string:
            result += '?' + query_string
        return result

    def test_eval_expr(self):
        response = self.app.get('/example1', status=500)
        debug_url = response.headers['X-Debug-URL']
        traceback_hash = debug_url.split('/')[-1]

        def make_url(frame_number, expr):
            return self._eval_expr_url(traceback_hash, expr, frame_number)

        def test_expr(frame_number, expr, expected_result):
            response = self.app.get(make_url(frame_number, expr))
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.content.strip(), expected_result)

        test_expr(0, '2+2', '4')
        test_expr(1, 'example1_view_local_var', "'local in example1()'")
        test_expr(2, 'foo_local_var', "'local in foo()'")
        test_expr(1, 'SomeModel.objects.all()[0].field', "u'test'")
        test_expr(1, 'from decimal import Decimal', "")
        test_expr(1, 'str(Decimal(0))', "'0'")

    def test_eval_expr_bad_requests(self):
        response = self.app.get('/example1', status=500)
        debug_url = response.headers['X-Debug-URL']
        traceback_hash = debug_url.split('/')[-1]

        url = self._eval_expr_url('not_traceback_hash', '1', 0)
        err_msg = 'No previously recorded exception'
        err_msg += 'trace matching traceback hash: not_traceback_hash'
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                url, status=500)

        url = self._eval_expr_url(traceback_hash=None, expr='1',
                                  frame_number=0)
        err_msg = 'Missing traceback_hash parameter'
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                url, status=500)

        url = self._eval_expr_url(traceback_hash='', expr='1', frame_number=0)
        err_msg = 'Empty traceback_hash parameter'
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                url, status=500)

        url = self._eval_expr_url(traceback_hash, '1', 3)
        err_msg = "Exception stack doesn't have frame number 3"
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                url, status=500)

        url = self._eval_expr_url(traceback_hash, '1', None)
        err_msg = 'Missing stack_frame parameter'
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                url, status=500)

        url = self._eval_expr_url(traceback_hash, '1', '')
        err_msg = 'Empty stack_frame parameter'
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                url, status=500)

        url = self._eval_expr_url(traceback_hash, '1', -1)
        err_msg = 'Invalid stack frame number: -1'
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                url, status=500)

        url = self._eval_expr_url(traceback_hash, '1', 'aaa')
        err_msg = 'Invalid stack frame number: aaa'
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                url, status=500)

        url = self._eval_expr_url(traceback_hash, None, 0)
        err_msg = 'Missing expr parameter'
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                url, status=500)

        url = self._eval_expr_url(traceback_hash, '', 0)
        err_msg = 'Empty expr parameter'
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                url, status=500)

    def test_traceback_info(self):
        def foo(x):
            try:
                exec 'y = 3; raise Exception()' in {}
            except:
                _, _, tb = sys.exc_info()
            return tb

        result = utils.traceback_info(foo(2))
        self.assertEqual(2, len(result))
        self.assertEqual('django_debugger.tests', result[0]['module_name'])
        self.assertTrue('django_debugger/tests.py' in result[0]['file_path'])
        self.assertEqual('foo', result[0]['function_name'])
        self.assertEqual('2', result[0]['local_vars']['x'])
        self.assertEqual('3', result[1]['global_vars']['y'])

    def test_view_traceback(self):
        self.app.get('/debug/view_traceback', status=404)
        self.app.get('/debug/view_traceback/', status=404)

        err_msg = 'No previously recorded exception'
        err_msg += 'trace matching traceback hash: abc'
        self.assertRaisesRegexp(Exception, err_msg, self.app.get,
                                '/debug/view_traceback/abc', status=500)

        response = self.app.get('/example1', status=500)
        # debug_url = response.headers['X-Debug-URL']
        # traceback_hash = debug_url.split('/')[-1]
        # self.assertTrue(traceback_hash in response.content)
        self.assertEqual(response.context['exception_header'],
                         'Exception: oh noez')
        self.assertTrue('Exception: oh noez' in response.content)
        self.assertTrue('test_app.views' in response.content)
        self.assertTrue('test_app.util' in response.content)
        self.assertTrue('foo' in response.content)
        self.assertTrue('example1' in response.content)


class SeleniumTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        cls.display = Display(visible=0, size=(800, 600))
        cls.display.start()
        cls.selenium = WebDriver()
        settings.DEBUG = True
        super(SeleniumTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        super(SeleniumTests, cls).tearDownClass()
        cls.selenium.quit()
        cls.display.stop()

    def test_login(self):
        self.selenium.get(self.live_server_url + '/example1')
        self.assertEqual(self.selenium.title, 'Server Error')
