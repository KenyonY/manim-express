from manimlib import *


def neural_network(each_layer_cell_num=(2, 3, 1),
                   interval=(0.5, 1),
                   top_pos=ORIGIN,
                   include_top=True,
                   top_layer_pos_list=None,
                   color=WHITE,
                   opacity=0.6,
                   style=0,
                   cell_size=1):
    """ Generate neural network graph.

    Args:
        each_layer_cell_num: Points the number of cell in each layer.
        interval: (x, y) interval of each cell.
        top_pos: The top layer's position if `include`_top is True.
        include_top: Is or Not include top layer.
        top_layer_pos_list: Points each cell's position in top layer.
                            (Valid only if parameter `include_top` is false.)
        color: Every cell's color.
        opacity: every cell's opacity.
        style: cell's style.

    Returns:
        Neural network graph `VGroup`.
    """

    def get_one_layer(pos=ORIGIN, num=10):
        if style == 0:
            cell = Dot().set_fill(color=color, opacity=opacity)
        elif style == 1:
            cell = Circle(radius=1).set_stroke(color, opacity=opacity, width=0.5*cell_size)\
                .scale(0.1*cell_size).set_fill(color, opacity=0.5)
        elif style == 2:
            cell = Circle(radius=1).set_stroke(color, opacity=opacity, width=0.5*cell_size)\
                .scale(0.1*cell_size)
        else:
            raise ValueError("style value error, options:0, 1, 2")

        one_layer = VGroup()
        pos_list = []
        d_shift = RIGHT*interval[0]
        shift_length = (num-1) * d_shift
        shift_pos = pos - shift_length/2
        for i in range(num):
            ceilcopy = cell.copy().shift(shift_pos)
            one_layer.add(ceilcopy)
            pos_list.append(ceilcopy.get_center())
            cell.shift(RIGHT*interval[0])

        return one_layer, pos_list
    layers = VGroup()
    if include_top:
        top_layer, top_layer_pos_list = get_one_layer(top_pos, each_layer_cell_num[0])
        layers.add(top_layer)
    else:
        assert top_layer_pos_list is not None
        top_layer_pos_list = top_layer_pos_list

    def add_one_layer(upper_layer_pos_list, pos, num):
        last_layer, last_pos_list = get_one_layer(pos, num=num)
        lines = VGroup()

        for upper_pos in upper_layer_pos_list:
            for last_pos in last_pos_list:
                line = Line(upper_pos, last_pos).set_stroke(width=0.6, opacity=0.66)
                lines.add(line)

        lines.add(last_layer)
        return lines, last_pos_list

    layer_pos_list = top_layer_pos_list
    for ceil_num in each_layer_cell_num[1:]:
        pos_center = (layer_pos_list[-1] + layer_pos_list[0])/2 + DOWN * interval[1]
        layer, layer_pos_list = add_one_layer(layer_pos_list, pos=pos_center, num=ceil_num)
        layers.add(layer)

    return layers
