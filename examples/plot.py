from example_imports import *

theta = np.linspace(-10, 2*PI, 1000)
x = np.cos(theta)
y = np.sin(theta)

# matplotlib
plt.plot(x, y, color='green', linewidth=2)
plt.plot(theta, x)
plt.axis('equal')
plt.show()

# manim_express
SceneArgs.color = "#222222"
scene = EagerModeScene(screen_size=Size.bigger)

scene.plot(theta, x, color=BLUE,  width=1)
scene.plot(x, y, color=GREEN_A, axes_ratio=1, show_axes=False)
# mob = scene.get_plot_mobj().move_to(UR*3)
# scene.add(mob)
scene.show_plot()

scene.hold_on()
