import os
import sys


def path(string: str) -> str:
    """Adaptive to different platforms """
    platform = sys.platform.lower()
    if 'linux' in platform:
        return string.replace('\\', '/')
    elif 'win' in platform:
        return string.replace('/', '\\')
    else:
        return string


def ppath(string, file=__file__) -> str:
    """Path in package"""
    return path(os.path.join(os.path.dirname(file), string))
