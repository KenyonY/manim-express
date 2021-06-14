from examples.example_imports import *
SceneArgs.use_online_tex = True

scene = EagerModeScene(screen_size=Size.big)
theta = np.linspace(0, TAU, 100)
x = np.cos(theta)
y = np.sin(theta)

scene.plot(theta, 2*y)

scene.plot(x, y, x_label='t', y_label='f(t)', axes_ratio=1)

scene.show_plot()

scene.hold_on()

