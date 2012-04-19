DEBUG = True

TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader',)

MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',
                      'django_debugger.middleware.DebuggerMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware')

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': 'db.sqlite'}}

ROOT_URLCONF = 'test_project.urls'

INSTALLED_APPS = ('django_debugger', 'test_app')

TEST_RUNNER = 'test_project.test_runner_with_coverage.CoverageTestRunner'
COVERAGE_MODULES = ['django_debugger.middleware',
                    'django_debugger.views',
                    'django_debugger.utils',
                    'django_debugger.tracebacks']
