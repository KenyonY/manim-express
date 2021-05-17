from express import EagerModeScene
from manimlib import *

scene = EagerModeScene(write_file=None, gif=False)

# circle = Circle(radius=0.5, arc_center=[0, 1, 0])
# axes = Axes()
#
# axes.add_coordinate_labels(
#     font_size=15,
# )
#
# g1 = axes.get_graph(lambda x: np.sin(x), [-5, 5])
# r = 2
# origin = [1, 1, 0]
#
# g2 = ParametricCurve(lambda theta: axes.c2p(*np.array([
#     r * np.cos(theta) + origin[0],
#     r * np.sin(theta) + origin[1],
#     ])),
#     [0, 2*TAU],
#     color = YELLOW
#                      )
# g1.set_color(YELLOW)
# scene.add(axes)
# scene.add(g1)
# scene.play(ShowCreation(g2))
#
# circle.move_to(axes.c2p(2, 0))
#
# circle.set_fill(BLUE, opacity=0.5)
# circle.set_stroke(BLUE_E, width=4)
# square = Square()
#
# scene.play(ShowCreation(square))
# # scene.wait()
# # # scene.play(ReplacementTransform(square, circle))
# # # scene.wait()
# # #
# # # # Stretched 4 times in the vertical direction
# # # scene.play(circle.animate.stretch(4, dim=0))
# # # scene.play(circle.animate.stretch(2, dim=1))
# # # # Rotate the ellipse 90°
# # # scene.play(Rotate(circle, TAU / 4))
# # # # Move 2 units to the right and shrink to 1/4 of the original
# # # scene.play(circle.animate.shift(2 * RIGHT), circle.animate.scale(0.25))
# # # # Insert 10 curves into circle for non-linear transformation (no animation will play)
# # # circle.insert_n_curves(20)
# # Apply a complex transformation of f(z)=z^2 to all points on the circle
# # scene.play(circle.animate.apply_complex_function(lambda z: 1/(z**2)))

# scene.tear_down()
scene.hold_on()
