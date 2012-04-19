import inspect


def get_frame_from_traceback(traceback, frame_number):
    ''' Returns n-th frame object from traceback.
        Returns None, if traceback doesn't have frame with such number.
    '''
    frames = inspect.getinnerframes(traceback)
    try:
        return frames[frame_number][0]
    except IndexError:
        return None
