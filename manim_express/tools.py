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


def calc_number_digit(number):
    res = number
    digit = 0
    if res >= 1:
        while res > 10:
            digit += 1
            # res, mod = np.divmod(res, 10)
            res //= 10
    else:
        while res < 1:
            digit -= 1
            res *= 10
    return 10**digit


def calc_number_step(number):
    digit = calc_number_digit(number)
    N = number / digit
    while True:
        if N < 5:
            digit /= 5
            N = round(number / digit)
        elif N > 10:
            digit *= 2
            N = round(number / digit)
        else:
            break
    return N, digit
