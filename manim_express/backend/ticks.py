import numpy as np
from rich import print
from collections import namedtuple

TickAttr = namedtuple("TickAttr",
                      ['tick_interval', 'axis_range', 'fmt', 'decimals', 'tick_values'])


class Ticker:
    def __init__(self, data, axis_length=400, tick_pixel=50):
        data_min, data_max = np.min(data), np.max(data)
        print(f"{data=}")
        self._axis_length = axis_length
        self._raw_interval = self._get_raw_interval(data_min, data_max, tick_pixel=tick_pixel)
        self.tick_attr = self._responsive_ticks(data_min, data_max)

    def ticks(self):
        # return [self.tick_attr.fmt.format(i) for i in self.tick_attr.tick_values]
        return self.tick_attr.tick_values

    def _get_raw_interval(self, data_min, data_max, tick_pixel=50):
        num_ticks = self._axis_length // tick_pixel
        return (data_max - data_min) / num_ticks

    def _calculate_interval(self):
        """
        Adjust the given interval to a human-friendly value.
        """
        magnitude = 10 ** np.floor(np.log10(self._raw_interval))
        possible_intervals = [1, 2, 5, 10]

        # Normalize the raw interval
        normalized_interval = self._raw_interval / magnitude

        # Find the closest friendly value
        friendly_value = min(possible_intervals, key=lambda x: abs(x - normalized_interval))

        return friendly_value * magnitude

    def _responsive_ticks(self, data_min, data_max):
        """
        Determine axis range, tick intervals, and label format based on data and axis length,
        ensuring that the tick values are human-friendly.
        """

        tick_interval = self._calculate_interval()
        print(f"{data_min=} {data_max=}")
        print(f"{tick_interval=}")
        axis_min = np.floor(data_min / tick_interval) * tick_interval
        axis_max = np.ceil(data_max / tick_interval) * tick_interval

        axis_range = (axis_min, axis_max)
        print(f"{axis_range=}")
        tick_values = np.arange(axis_min, axis_max, tick_interval)

        if tick_interval.is_integer():
            label_format = "{:.0f}"
            decimals = 0 # todo
        else:
            decimals = int(-np.log10(tick_interval - int(tick_interval))) + 1
            label_format = "{:." + str(decimals) + "f}"

        return TickAttr(tick_interval=tick_interval,
                        axis_range=axis_range,
                        fmt=label_format,
                        decimals=decimals,
                        tick_values=tick_values)


def test1():
    test_cases = {
        "Narrow Range": [100, 100.1, 100.2, 100.3],
        "Wide Range": [-1e6, 1e6],
        "Negative Values": [-2002, -1000],
        "Small Values": [0.001, 0.002, 0.003],
        "Normal Range": [0, 50, 100, 150]
    }
    further_test_cases = {
        "Large Numbers": [1e8, 1.5e8, 2e8, 2.5e8, 3e8],
        "Very Small Decimals": [0.00001, 0.000015, 0.00002, 0.000025, 0.00003],
        "Mixed Large Positive and Negative": [-1e6, -5e5, 0, 5e5, 1e6],
        "Mixed Small Positive and Negative": [-0.003, -0.002, 0, 0.002, 0.003],
        "Huge Numbers": [1e12, 1.2e12, 1.4e12, 1.6e12, 1.8e12],
        "Tiny Decimals": [1e-8, 2e-8, 3e-8, 4e-8, 5e-8],
        "lal1": [2.5, 5.8, 9.1, 12.6, 15.3, 18.7],
        "lal2": [-1002.5, 5.8, 9.1, 12.6, 15.3, 18.7],
        "lal3": [0.41235, 5.2348, 9.231, 12.3246, 15.3423, 18.17],
    }
    friendly_results = {}
    sample_data = [2.5, 5.8, 9.1, 12.6, 15.3, 18.7]
    axis_length = 200
    for name, data in further_test_cases.items():
        friendly_results[name] = Ticker(data).tick_attr

    print(friendly_results)
    for key, value in friendly_results.items():
        axis_range, tick_interval, label_format, tick_values = value
        print([label_format.format(i) for i in tick_values])


# Run the tests for the optimized version
# test1()
