import hashlib


class TraceBacks(object):
    ''' Mapping from unique strings to exception tracebacks.
    '''

    def __init__(self):
        self._tracebacks = {}

    @staticmethod
    def traceback_hash(traceback):
        md5 = hashlib.md5()
        md5.update(str(hash(traceback)))
        return md5.hexdigest()

    def add_traceback(self, traceback, exception):
        '''
        Adds an exception traceback (including exception),
        and returns str with unique id for this traceback.
        '''
        traceback_hash = self.traceback_hash(traceback)
        self._tracebacks[traceback_hash] = (traceback, exception)
        return traceback_hash

    def get_traceback(self, traceback_hash):
        '''
        Returns tuple with previously added traceback and its exception.
        traceback_hash is a str returned by add_traceback().
        Returns None, if there's no traceback with provided traceback_hash.
        '''
        return self._tracebacks.get(traceback_hash)

    def number_of_tracebacks(self):
        '''
        Returns int with the number of stored exception tracebacks.
        '''
        return len(self._tracebacks)
