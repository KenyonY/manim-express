import numpy as np

from examples.example_imports import *

# SceneArgs.color = "#ffffff"
scene = EagerModeScene()
text = Text("hello, world", t2g={"world": (RED, BLUE),
                                 "hel": (BLACK, GREEN, YELLOW)}).move_to(UP*3)
scene.add(text)

rod_start = np.array([0, 0, 0])
rod_end = np.array([-1, -0, 0])
fixed_point = Sphere(radius=0.1).set_color(GREEN).move_to(rod_start)
rod = Line3D(rod_start, rod_end, width=0.1)
rod.set_color(RED)
scene.add(fixed_point)
scene.play(ShowCreation(rod))

T = 0

def update_pendulum(x, dt):
    global T
    dt *= 5
    T += dt
    pos = x.get_end()


    x.rotate_about_origin(dt * np.sin(T))


rod.add_updater(update_pendulum)
scene.wait(10)

text = Text("I'm Text.").set_color(GREEN)
text.save_state()


def my_rotate(obj, alpha):
    obj.restore()
    obj.shift(RIGHT * 2 * alpha)
    obj.rotate(alpha * TAU)


scene.play(UpdateFromAlphaFunc(text, my_rotate))

scene.hold_on()
