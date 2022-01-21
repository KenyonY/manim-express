import numpy as np
import time
import random
import math
from scipy.signal import savgol_filter, spline_filter, order_filter, qspline1d, qspline1d_eval, medfilt
# import cv2


def random_trigonometric(x, n=5, w_min=3, w_max=20, intensity=0.003):
    """周期为PI, 很尴尬"""
    # theta = np.linspace(0, np.pi * 2, N)
    N = len(x)
    delta_w = w_max - w_min
    wave = np.array([0.] * N)
    for i in range(n):
        w = w_min + random.random() * delta_w
        phi = np.random.rand() * 2 * np.pi * w
        pth_pwave = np.sin(w * x + phi) * intensity
        wave += pth_pwave
    return wave


def rand_func(t, intensity=0.003):
    """
    方案一: 随机生成len(t)个随机数, 然后先中值滤波, 在均值滤波
    方案二: 随机生成固定个随机数(如20个), 然后对其差值到len(t)个.

    Args:
        t:
        intensity:

    Returns:

    """
    N = len(t)
    # x_noisy = np.random.normal(intensity, size=N)
    np.random.seed(int(time.time()))
    x_noisy = np.random.rand(N) * intensity
    min_cutoff = 0.4
    beta = 0.01
    # x_hat = np.zeros_like(x_noisy)
    # x_hat[0] = x_noisy[0]
    # one_euro_filter = OneEuroFilter(
    #     t[0], x_noisy[0],
    #     min_cutoff=min_cutoff,
    #     beta=beta
    # )
    # for i in range(1, N):
    #     x_hat[i] = one_euro_filter(t[i], x_noisy[i])

    kernel_size = N//20
    if kernel_size % 2 == 0:
        kernel_size += 1
    f1 = medfilt(x_noisy, kernel_size)
    res = t + move_avg(f1, kernel_size)
    res[-1] = t[-1]
    res[0] = t[0]
    return res


def move_avg(t, n=5):
    return np.convolve(t, np.ones((n,)) / n, mode='same')


def smoothing_factor(t_e, cutoff):
    r = 2 * math.pi * cutoff * t_e
    return r / (r + 1)


def exponential_smoothing(a, x, x_prev):
    return a * x + (1 - a) * x_prev


class OneEuroFilter:
    def __init__(self, t0, x0, dx0=0.0, min_cutoff=1.0, beta=0.0,
                 d_cutoff=1.0):
        """Initialize the one euro filter."""
        # The parameters.
        self.min_cutoff = float(min_cutoff)
        self.beta = float(beta)
        self.d_cutoff = float(d_cutoff)
        # Previous values.
        self.x_prev = float(x0)
        self.dx_prev = float(dx0)
        self.t_prev = float(t0)

    def __call__(self, t, x):
        """Compute the filtered signal."""
        t_e = t - self.t_prev

        # The filtered derivative of the signal.
        a_d = smoothing_factor(t_e, self.d_cutoff)
        dx = (x - self.x_prev) / t_e
        dx_hat = exponential_smoothing(a_d, dx, self.dx_prev)

        # The filtered signal.
        cutoff = self.min_cutoff + self.beta * abs(dx_hat)
        a = smoothing_factor(t_e, cutoff)
        x_hat = exponential_smoothing(a, x, self.x_prev)

        # Memorize the previous values.
        self.x_prev = x_hat
        self.dx_prev = dx_hat
        self.t_prev = t

        return x_hat
