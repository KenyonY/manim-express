import numpy as np


class Ticker:
    def __init__(self, x_series, steps_range=(5, 10)):
        self.x_max = max(x_series)
        self.x_min = min(x_series)
        self.step_range = set(range(steps_range[0], steps_range[1]+1))
        self.delta_x = self.x_max - self.x_min
        self.valid_number, self.exp_number = self.number_to_valid_and_exp(self.delta_x)
        self.epsilon = 1e-4 * self.delta_x
        self.x_min -= self.epsilon

    @staticmethod
    def number_to_valid_and_exp(number):
        s = np.format_float_scientific(number, precision=6)
        valid_number_str, exp_number_str = s.split('e')
        exp_number = float('1e' + exp_number_str)
        valid_number = float(valid_number_str)
        return valid_number, exp_number

    @staticmethod
    def _staircase():
        steps = (1, 2, 2.5, 5, 10)
        steps_array = np.asarray(steps)
        flights = (0.1 * steps_array[:-1], steps_array, 10 * steps_array[1])
        return np.hstack(flights)

    def calc_step(self, steps):
        offset_min = float("inf")
        best_n_step, best_step = 0, None
        for step in steps:
            n_step = round(self.valid_number / step)
            if n_step in self.step_range:
                x_offset = self.valid_number - n_step * step
                if best_n_step < n_step:
                    offset_min = x_offset
                    best_n_step, best_step = n_step, step

        return best_n_step, best_step, offset_min

    def get_start_tick(self, step):
        _, mod = np.divmod(self.x_min, step)
        print("mod, step")
        print(mod, step)
        return self.x_min + (step - mod)

    def ticks(self):
        valid_number, exp_number = self.number_to_valid_and_exp(self.delta_x)
        steps = self._staircase()
        n_step, step, x_offset = self.calc_step(steps)
        step = step * exp_number
        print("step:", step, )

        start_tick = self.get_start_tick(step)
        print(start_tick)
        tick_list = []
        for idx in range(n_step):
            tick_list.append(round(start_tick + idx * step, 7))
        return tick_list


a = np.linspace(-1.30, 234.1234, 100)
ticker = Ticker(a, step_range=(5, 9))
res = ticker.ticks()
print(res)

import matplotlib.pyplot as plt

plt.plot(a, np.sin(a))
plt.show()
