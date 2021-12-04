from examples.example_imports import *
CONFIG.use_online_tex = True


scene = EagerModeScene(screen_size=Size.bigger)
theta = np.linspace(0, TAU, 100)


x = np.array([0.2,0.9])
y = np.array([0.1, 0.3])


def calc_avg_slope(x: np.ndarray, y: np.ndarray):
    k_array = np.array([yi/xi for xi, yi in zip(x, y)])
    k1 = k_array.mean()
    print(k1)

    k2 = y.mean()/x.mean()
    print(k2)





# x = np.cos(theta)
# y = np.sin(theta)

# scene.plot(x, y)

# scene.plot(x, y,
#            x_label='t', y_label='f(t)',
#            scale_ratio=1,
#            )
#
# scene.show_plot()
# scene.hold_on()

calc_avg_slope(y, x)
