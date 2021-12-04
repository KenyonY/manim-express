from manimlib import *
from ..color import color_list


class NeuralNetwork:
    def __init__(self,
                 each_layer_cell_num=(2, 3, 1),
                 interval=(0.5, 1),
                 top_pos=ORIGIN,
                 include_top=True,
                 top_layer_pos_list=None,
                 color=WHITE,
                 opacity=0.6,
                 style=0,
                 cell_size=1
                 ):
        """Generate neural network graph.
        Args:
            each_layer_cell_num: Points the number of cell in each layer.
            interval: (x, y) interval of each cell.
            top_pos: The top layer's position if `include_top` is True.
            include_top: Is or Not include top layer.
            top_layer_pos_list: Points each cell's position in top layer. (Valid only
            if parameter `include_top` is false.)
            color: Every cell's color.
            opacity: every cell's opacity.
            style: cell's style.
            cell_size:
        """
        self._layers = VGroup()

        self._color = color
        self._opacity = opacity
        self._interval = interval
        self._style = style
        self._cell_size = cell_size
        self._include_top = include_top
        self._top_pos = top_pos
        self._layer_lines = VGroup()
        self._layer_cells = VGroup()

        if self._include_top:
            top_layer, top_layer_pos_list = self.one_layer_cells(self._top_pos, each_layer_cell_num[0])
            self._layers.add(top_layer)
            self._layer_cells.add(top_layer)
        else:
            assert top_layer_pos_list is not None
        layer_pos_list = top_layer_pos_list
        for ceil_num in each_layer_cell_num[1:]:
            layer_line_cell, layer_pos_list = self.add_one_layer(layer_pos_list, num=ceil_num)
            self._layers.add(layer_line_cell)

    def get_graph(self):
        return self._layers
    
    def get_lines(self):
        return self._layer_lines
    
    def get_cells(self):
        return self._layer_cells

    def set_layer_cell_text(self, n, weights=np.random.random(10), textsize=0.26):
        print(len(self._layer_cells.submobjects))
        texts = VGroup()
        for idx, cell in enumerate(self._layer_cells.submobjects[n]):
            cell: Mobject
            text = TexText(f"{weights[idx]:.1f}").move_to(cell.get_center()).scale(self._cell_size*textsize)
            texts.add(text)
        self._layers.add(texts)
    
    def set_layer_line(self, n, weights=None):
        lines = self._layer_lines.submobjects
        layer_cells = self._layer_cells.submobjects
        if weights is None:
            try:
             weights = np.random.rand(len(layer_cells[n]), len(layer_cells[n+1]))
            except IndexError:
                pass
        for line in lines[n]:
            line: Line
            color = np.random.choice(color_list, 1)[0]
            line.set_color(color=color)

    def one_layer_cells(self, pos=ORIGIN, num=10):
        if self._style == 0:
            cell = Dot().set_fill(color=self._color, opacity=self._opacity)
        elif self._style == 1:
            cell = Circle(radius=1).set_stroke(self._color, opacity=self._opacity, width=0.5*self._cell_size)\
                .scale(0.1*self._cell_size).set_fill(self._color, opacity=self._opacity)
        elif self._style == 2:
            cell = Circle(radius=1).set_stroke(self._color, opacity=self._opacity, width=0.5*self._cell_size)\
                .scale(0.1*self._cell_size)
        else:
            raise ValueError("`style` value error, options:0, 1, 2")

        one_layer = VGroup()
        pos_list = []
        d_shift = RIGHT*self._interval[0]
        shift_length = (num-1) * d_shift
        shift_pos = pos - shift_length/2
        for i in range(num):
            ceilcopy = cell.copy().shift(shift_pos)
            one_layer.add(ceilcopy)
            pos_list.append(ceilcopy.get_center())
            cell.shift(RIGHT*self._interval[0])

        return one_layer, pos_list

    def add_one_layer(self, upper_layer_pos_list, num):
        center_pos = (upper_layer_pos_list[-1] + upper_layer_pos_list[0]) / 2 + DOWN * self._interval[1]
        last_layer_cell, last_pos_list = self.one_layer_cells(center_pos, num=num)
        self._layer_cells.add(last_layer_cell)
        lines = VGroup()
        layer_line_cell = VGroup()
        for upper_pos in upper_layer_pos_list:
            for last_pos in last_pos_list:
                line = Line(upper_pos, last_pos, buff=1*0.1*self._cell_size).set_stroke(width=1, opacity=0.66)
                lines.add(line)

        self._layer_lines.add(lines)
        layer_line_cell.add(lines)
        layer_line_cell.add(last_layer_cell)
        return layer_line_cell, last_pos_list

