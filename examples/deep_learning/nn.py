from examples.example_imports import *
from manim_express.nn.network import NeuralNetwork

warnings.filterwarnings('ignore')

# CONFIG.use_online_tex=True
scene = EagerModeScene(screen_size=Size.bigger)
top_layer = VGroup()
[top_layer.add(Dot([i, 2, 0], color=YELLOW_B)) for i in range(4)]
scene.add(top_layer)
print(top_layer.get_all_points())

nn = NeuralNetwork((5, 10, 1),
                   interval=(0.5, 1),
                   include_top=False,
                   top_layer_pos_list=[np.array([i, 2, 0]) for i in range(4)],
                   color=WHITE,
                   opacity=1,
                   style=2,
                   cell_size=2,
                   )


# scene.play(Write(nn.get_cells()))
# scene.play(Write(nn.get_lines()))
nn.set_layer_cell_text(1)
nn.set_layer_line(1, )
scene.play(Write(nn.get_graph()), run_time=5)

#
# print(scene.num_plays)
# scene.hold_on()
#
# circle = Circle().move_to(RIGHT*3)
# scene.play(ShowCreation(circle))
#
# print(scene.num_plays)
# scene.hold_on()


print(scene.num_plays)

scene.hold_on()

