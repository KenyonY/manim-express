import numpy as np


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
    return 10 ** digit


def calc_number_step(number):
    digit = calc_number_digit(number)
    n = number / digit
    while True:
        if n < 5:
            digit /= 5
            n = round(number / digit)
        elif n > 10:
            digit *= 2
            n = round(number / digit)
        else:
            break
    return n, digit
