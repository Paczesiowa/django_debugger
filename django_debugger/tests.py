import sys

from django.test import TestCase
from django_debugger.tracebacks import TraceBacks


class TraceBacksTest(TestCase):

    def test_tracebacks(self):
        tbs = TraceBacks()
        tbs2 = TraceBacks()
        self.assertEqual(id(tbs), id(tbs2))

        try:
            raise Exception()
        except:
            _, _, tb = sys.exc_info()

        hash_ = tbs.add_traceback(tb)
        self.assertEqual(type(hash_), str)
        self.assertEqual(id(tb), id(tbs.get_traceback(hash_)))
        self.assertIsNone(tbs.get_traceback('foo'))
