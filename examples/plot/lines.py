from examples.example_imports import *
scene = EagerModeScene(screen_size=Size.bigger)

graph = Line().scale(0.2)
t0 = time.time()

delta_t = 0.5
for a in np.linspace(3, 12, 3):
    graph2= ParametricCurve(lambda t: [t,
                                       0.8*np.abs(t)**(6/7) + 0.9*np.sqrt(abs(a-t**2)) * np.sin(a*t +0.2),
                                       0],
                            t_range=(-math.sqrt(a), math.sqrt(a))).scale(0.5)
    scene.play(Transform(graph, graph2), run_time = 3)

scene.hold_on()