# This file comes from WebError library (http://pypi.python.org/pypi/WebError)

from cStringIO import StringIO
import traceback
import threading
import sys

exec_lock = threading.Lock()


class EvalContext(object):

    """
    Class that represents a interactive interface.  It has its own
    namespace.  Use eval_context.exec_expr(expr) to run commands; the
    output of those commands is returned, as are print statements.

    This is essentially what doctest does, and is taken directly from
    doctest.
    """

    def __init__(self, namespace, globs):
        self.namespace = namespace
        self.globs = globs

    def exec_expr(self, s):
        out = StringIO()
        exec_lock.acquire()
        save_stdout = sys.stdout
        try:
            sys.stdout = out
            try:
                code = compile(s, '<web>', "single", 0, 1)
                exec code in self.namespace, self.globs
            except KeyboardInterrupt:
                raise
            except:
                traceback.print_exc(file=out)
        finally:
            sys.stdout = save_stdout
            exec_lock.release()
        return out.getvalue()
