import hashlib


class TraceBacks(object):
    ''' Mapping from unique strings to exception tracebacks.
    '''

    def __init__(self):
        self._tracebacks = {}

    def _traceback_hash(self, traceback):
        md5 = hashlib.md5()
        md5.update(str(hash(traceback)))
        return md5.hexdigest()

    def add_traceback(self, traceback):
        '''
        Adds an exception traceback, and returns str with unique id
        for this traceback.
        '''
        traceback_hash = self._traceback_hash(traceback)
        self._tracebacks[traceback_hash] = traceback
        return traceback_hash

    def get_traceback(self, traceback_hash):
        '''
        Returns previously added traceback.
        traceback_hash is a str returned by add_traceback().
        Returns None, if there's no traceback with provided traceback_hash.
        '''
        return self._tracebacks.get(traceback_hash)
