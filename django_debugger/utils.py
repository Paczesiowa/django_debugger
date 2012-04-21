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


def format_exception_header(exception):
    ''' Returns str like: Exception: message
        >>> format_exception_header(Exception([0]))
        'Exception: [0]'
    '''
    result = exception.__class__.__name__
    result += ': ' + str(exception.message)
    return result


def traceback_info(traceback):
    ''' Returns info about exception traceback stack frames.

        Returns a list with the following dict for every frame
        (where execution stopped in that frame):
        * module_name: str with module name
        * file_path: str with absolute path to that module
        * line_number: int with line numbername
        * function_name: str with function_name
        * local_vars: dict mapping local variable name to
             its str representation (__builtins__ are stripped)
        * global_vars: dict mapping global variable name to
             its str representation (__builtins__ are stripped)

        module_name, file_path can be None.
    '''
    result = []

    def format_dict(d):
        result = {}
        for k, v in d.items():
            result[k] = str(v)
        return result

    for elem in inspect.getinnerframes(traceback):
        frame = elem[0]
        frame_info = {}

        module = inspect.getmodule(frame)
        frame_info['module_name'] = module.__name__ if module else None
        frame_info['file_path'] = module.__file__ if module else None
        frame_info['line_number'] = frame.f_lineno
        frame_info['function_name'] = frame.f_code.co_name
        locals_copy = frame.f_locals.copy()
        if '__builtins__' in locals_copy:
            del locals_copy['__builtins__']
        frame_info['local_vars'] = format_dict(locals_copy)
        globals_copy = frame.f_globals.copy()
        del globals_copy['__builtins__']
        frame_info['global_vars'] = format_dict(globals_copy)
        result.append(frame_info)

    return result
