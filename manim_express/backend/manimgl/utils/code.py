from manimlib import *

__all__ = ['get_code_by_read']


def get_code_by_read(code_path, language='python', **kwargs):
    with open(code_path, 'r') as fr:
        code_string = fr.read().strip('\n')
    return Code(code_string, language=language, **kwargs)
