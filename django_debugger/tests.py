import sys

from django.test import TestCase
from django_debugger.tracebacks import TraceBacks


class DjangoDebuggerTest(TestCase):

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
