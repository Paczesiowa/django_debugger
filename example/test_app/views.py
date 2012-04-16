import test_app.util as util


def example1(request):
    example1_view_local_var = 'local in example1()'
    util.foo()  # this raises exception
