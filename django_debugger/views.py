from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django_debugger.evalcontext import EvalContext
from django_debugger.utils import get_frame_from_traceback


def view_traceback(request, traceback_hash):
    ctx = {'traceback_hash': traceback_hash}
    response = render(request, 'django_debugger/view_traceback.html',
                      ctx, status=500)
    self_url_path = reverse('view_traceback', kwargs={'traceback_hash':
                                                          traceback_hash})
    self_url = request.build_absolute_uri(self_url_path)
    response['X-Debug-URL'] = self_url
    return response


def this_always_fails(request):
    ''' This view always throws exception.
        It's used in tests, to check if the middleware passes through
        exception originating from this app.
    '''
    raise Exception('I failed')


def eval_expr(request):
    ''' Evaluates an expression and returns it's result.

        GET params:
        * traceback_hash: str with hash of an exception traceback,
             that was previously thrown (in this application run)
        * frame_number: non-negative stack frame number in which
             code should be run, cannot be greater than number
             of stack frames in an exception traceback (0-based)
        * expr: str with an expression to evaluate.
    '''
    traceback_hash = request.GET.get('traceback_hash')
    if traceback_hash is None:
        raise Exception('Missing traceback_hash parameter')
    if traceback_hash == '':
        raise Exception('Empty traceback_hash parameter')
    traceback = request.debugger_middleware_state.tracebacks\
                       .get_traceback(traceback_hash)
    if traceback is None:
        err_msg = 'No previously recorded exception'
        err_msg += 'trace matching traceback hash: ' + traceback_hash
        raise Exception(err_msg)

    frame_number = request.GET.get('frame_number')
    if frame_number is None:
        raise Exception('Missing stack_frame parameter')
    if frame_number == '':
        raise Exception('Empty stack_frame parameter')
    try:
        frame_number = int(frame_number)
    except ValueError:
        raise Exception('Invalid stack frame number: ' + frame_number)
    if frame_number < 0:
        raise Exception('Invalid stack frame number: ' + str(frame_number))

    frame = get_frame_from_traceback(traceback, frame_number)
    if frame is None:
        err_msg = "Exception stack doesn't have frame number "
        err_msg += str(frame_number)
        raise Exception(err_msg)

    expr = request.GET.get('expr')
    if expr is None:
        raise Exception('Missing expr parameter')
    if expr == '':
        raise Exception('Empty expr parameter')

    ec = EvalContext(frame.f_locals, frame.f_globals)
    res = ec.exec_expr(expr)
    return HttpResponse(res)
