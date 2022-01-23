import numpy as np


def get_num_digit(number):
    int_part, frac_part = str(float(number)).split(".")
    int_digit, frac_digit = len(int_part), len(frac_part)
    if frac_part == '0':
        frac_digit = 0
    if int_part == '0':
        int_digit = 0
    return int_digit, frac_digit





def _staircase():
    steps = np.array([1, 2, 2.5, 5, 10])
    flights = (0.1 * steps[:-1], steps, 10 * steps[1])
    return np.hstack(flights)


def ticks(x_range):
    x_max = max(x_range)
    x_min = min(x_range)
    delta_x = x_max - x_min
    int_digits, frac_digits = get_num_digit(delta_x)



a = np.linspace(0, 2 * np.pi, 100)
res = ticks(a)
print(res)
