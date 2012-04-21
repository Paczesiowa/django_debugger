DEBUG = True

TEMPLATE_LOADERS = ('django.template.loaders.app_directories.Loader',)

MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',
                      'django_debugger.middleware.DebuggerMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware')

DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                         'NAME': 'db.sqlite'}}

ROOT_URLCONF = 'test_project.urls'

INSTALLED_APPS = ('django_debugger', 'test_app')

TEST_RUNNER = 'django_coverage.coverage_runner.CoverageRunner'

# Only needed for tests, Django's LiveServerTestCase fails without these
STATIC_URL = '/static/'
MEDIA_URL = '/media/'
