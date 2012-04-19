import test_app.util as util
from test_app.models import SomeModel


def example1(request):
    example1_view_local_var = 'local in example1()'
    SomeModel(field='test').save()
    util.foo()  # this raises exception
