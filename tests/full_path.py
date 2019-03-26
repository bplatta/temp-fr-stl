import os.path

def get_full_path(file_obj, append_path=None):
    return '{}{}'.format(os.path.dirname(os.path.abspath(file_obj)), append_path or '')