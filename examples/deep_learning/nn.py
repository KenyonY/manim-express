from examples.example_imports import *
from manim_express.nn.network import NeuralNetwork


scene = EagerModeScene(screen_size=Size.bigger)
top_layer = VGroup()
[top_layer.add(Dot([i, 2, 0])) for i in range(4)]
scene.add(top_layer)

nn = NeuralNetwork((5, 10, 1),
                   interval=(0.5, 0.7),
                   include_top=True,
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
scene.play(Write(nn.get_graph().scale(1)))


print(scene.num_plays)
scene.hold_on()

circle = Circle().move_to(RIGHT*3)
scene.play(ShowCreation(circle))

print(scene.num_plays)
scene.hold_on()

scene.start_at_animation_number(0)
print(scene.num_plays)

scene.hold_on()

