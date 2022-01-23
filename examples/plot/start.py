from examples.example_imports import *
CONFIG.use_online_tex = True

scene = EagerModeScene()
theta = np.linspace(0, TAU, 100)

x = np.cos(theta)
y = np.sin(theta)

scene.plot(theta, y)

scene.plot(x, y,
           x_label='t', y_label='f(t)',
           scale_ratio=1,
           )

scene.show_plot()
scene.get_run_time()
scene.hold_on()

