from examples.example_imports import *
SceneArgs.use_online_tex = 0

scene = EagerModeScene(screen_size=Size.bigger)
theta = np.linspace(0, TAU, 100)

x = np.cos(theta)
y = np.sin(theta)

scene.plot(theta, y)

scene.plot(x, y, x_label='t', y_label='f(t)',
           scale_ratio=1,
           )

scene.show_plot()

scene.hold_on()

