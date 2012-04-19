import coverage
from django.conf import settings
from django.test.simple import DjangoTestSuiteRunner


class CoverageTestRunner(DjangoTestSuiteRunner):

    def run_tests(self, test_labels, extra_tests=None, **kwargs):
        if hasattr(settings, 'COVERAGE_MODULES'):
            coverage.use_cache(0)
            coverage.start()

        result = DjangoTestSuiteRunner.run_tests(self, test_labels,
                                                 extra_tests, **kwargs)

        if hasattr(settings, 'COVERAGE_MODULES'):
            coverage.stop()

        print ''
        print '------------------------------------------------------------'
        print ' Unit Test Code Coverage Results'
        print '------------------------------------------------------------'

        if hasattr(settings, 'COVERAGE_MODULES'):
            coverage_modules = []
            for module in settings.COVERAGE_MODULES:
                coverage_modules.append(__import__(module, globals(),
                                                   locals(), ['']))

            coverage.report(coverage_modules, show_missing=1)

        print '------------------------------------------------------------'

        return result
