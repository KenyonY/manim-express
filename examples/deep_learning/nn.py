from examples.example_imports import *
from manim_express.nn import network


scene = EagerModeScene()

top_layer = VGroup()
[top_layer.add(Dot([i, 2, 0])) for i in range(4)]
scene.add(top_layer)
nn = network.neural_network((5, 10, 1), include_top=False,
                            top_layer_pos_list=[np.array([i, 2, 0]) for i in range(4)],
                            color=WHITE,
                            opacity=1,
                            style=2,
                            cell_size=2)
scene.play(Write(nn))

scene.hold_on()
