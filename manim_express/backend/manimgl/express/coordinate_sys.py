from manimlib import *
from ...tick import Ticker
from typing import Tuple, Union, List


class SciNumberLine(NumberLine):

    def __init__(self, x_range: Union[Tuple, List], **kwargs):
        self.color = GREY_B
        self.stroke_width = 2
        # List of 2 or 3 elements, x_min, x_max, step_size
        self.x_range = x_range
        # How big is one one unit of this number line in terms of absolute spacial distance
        self.unit_size = 1
        self.width = FRAME_WIDTH - 2
        self.include_ticks = True
        self.tick_size = 0.1
        self.longer_tick_multiple = 1.5
        self.tick_offset = 0
        # Change name
        self.numbers_with_elongated_ticks = []
        self.include_numbers = False
        self.line_to_number_direction = DOWN
        self.line_to_number_buff = MED_SMALL_BUFF
        self.include_tip = True
        self.tip_config = {
            "width": 0.125,
            "length": 0.25,
        }
        self.decimal_number_config = {
            "num_decimal_places": 0,
            "font_size": 36,
        }
        self.numbers_to_exclude = None
        super().__init__(x_range=x_range, **kwargs)

    def get_tick_range(self):
        ticker = Ticker(self.x_min, self.x_max, steps_range=(5, 10))
        tick_list = ticker.ticks()
        tick_digit = ticker.get_tick_digit()
        if tick_digit > 0:
            num_decimal = 0
        else:
            num_decimal = -tick_digit
        self.decimal_number_config = {
            "num_decimal_places": num_decimal,
            "font_size": 36,
        }
        return tick_list

    def add_ticks(self):
        ticks = VGroup()
        for x in self.get_tick_range():
            size = self.tick_size
            if np.isclose(self.numbers_with_elongated_ticks, x).any():
                size *= self.longer_tick_multiple
            ticks.add(self.get_tick(x, size))
        self.add(ticks)
        self.ticks = ticks

    def add_numbers(self, x_values=None, excluding=None, font_size=24, **kwargs):
        if x_values is None:
            x_values = self.get_tick_range()

        kwargs["font_size"] = font_size

        if excluding is None:
            excluding = self.numbers_to_exclude

        numbers = VGroup()
        for x in x_values:
            if excluding is not None and x in excluding:
                continue
            numbers.add(self.get_number_mobject(x, **kwargs))
        self.add(numbers)
        self.numbers = numbers
        return numbers

class NewAxes(Axes):
    def __init__(self,
                 x_range=None,
                 y_range=None,
                 **kwargs):
        CoordinateSystem.__init__(self, **kwargs)
        VGroup.__init__(self, **kwargs)

        if x_range is not None:
            self.x_range[:len(x_range)] = x_range
        if y_range is not None:
            self.y_range[:len(y_range)] = y_range

        self.x_axis = self.create_axis(
            self.x_range, self.x_axis_config, self.width,
        )
        self.y_axis = self.create_axis(
            self.y_range, self.y_axis_config, self.height
        )
        self.y_axis.rotate(90 * DEGREES, about_point=ORIGIN)
        # Add as a separate group in case various other
        # mobjects are added to self, as for example in
        # NumberPlane below
        self.axes = VGroup(self.x_axis, self.y_axis)
        self.add(*self.axes)
        self.center()

    def create_axis(self, range_terms, axis_config, length):
        new_config = merge_dicts_recursively(self.axis_config, axis_config)
        new_config["width"] = length
        axis = NumberLine(range_terms, **new_config)
        axis.shift(-axis.n2p(0))
        return axis
