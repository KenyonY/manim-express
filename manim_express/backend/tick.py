import numpy as np


class Ticker:
    def __init__(self, x_min, x_max, steps_range=(5, 10)):
        self.x_max = x_max
        self.x_min = x_min
        self.step_range = set(range(steps_range[0], steps_range[1] + 1))
        self._delta_x = self.x_max - self.x_min
        self._valid_number, self._exp_number = self._number_to_valid_and_exp(self._delta_x)
        self._epsilon = 1e-4 * self._delta_x
        self.x_min -= self._epsilon
        self._start_tick, self._step = None, None

    def get_tick_digit(self):
        return int(np.format_float_scientific(self._step).split('e')[1])

    @staticmethod
    def _number_to_valid_and_exp(number):
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

    def _calc_step(self, steps):
        offset_min = float("inf")
        best_n_step, best_step = 0, None
        for step in steps:
            n_step = round(self._valid_number / step)
            if n_step in self.step_range:
                x_offset = self._valid_number - n_step * step
                if best_n_step < n_step:
                    offset_min = x_offset
                    best_n_step, best_step = n_step, step

        return best_n_step, best_step, offset_min

    def _get_start_tick(self, step):
        _, mod = np.divmod(self.x_min, step)
        return self.x_min + (step - mod)

    def get_start_and_step(self):
        return self._start_tick, self._step

    def ticks(self):
        valid_number, exp_number = self._number_to_valid_and_exp(self._delta_x)
        steps = self._staircase()
        n_step, step, x_offset = self._calc_step(steps)
        step = step * exp_number
        self._step = step
        start_tick = self._get_start_tick(step)
        self._start_tick = start_tick
        tick_list = []
        for idx in range(n_step):
            tick_list.append(round(start_tick + idx * step, 7))
        return tick_list
