DEBUG = True

TEMPLATE_LOADERS = ('django.template.loaders.filesystem.Loader',)

MIDDLEWARE_CLASSES = ('django.middleware.common.CommonMiddleware',
                      'django_debugger.middleware.DebuggerMiddleware',
                      'django.middleware.csrf.CsrfViewMiddleware')

ROOT_URLCONF = 'test_project.urls'

INSTALLED_APPS = ('django_debugger')
