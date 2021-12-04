import scipy.integrate
from example_imports import *
# from manim_imports_ext import *

scene = EagerModeScene(screen_size=Size.big)

USE_ALMOST_FOURIER_BY_DEFAULT = True
NUM_SAMPLES_FOR_FFT = 1000
DEFAULT_COMPLEX_TO_REAL_FUNC = lambda z : z.real


def get_fourier_graph(
    axes, time_func, t_min, t_max,
    n_samples = NUM_SAMPLES_FOR_FFT,
    complex_to_real_func = lambda z : z.real,
    color = RED,
    ):
    # N = n_samples
    # T = time_range/n_samples
    time_range = float(t_max - t_min)
    time_step_size = time_range/n_samples
    time_samples = np.vectorize(time_func)(np.linspace(t_min, t_max, n_samples))
    fft_output = np.fft.fft(time_samples)
    frequencies = np.linspace(0.0, n_samples/(2.0*time_range), n_samples//2)
    #  #Cycles per second of fouier_samples[1]
    # (1/time_range)*n_samples
    # freq_step_size = 1./time_range
    graph = VMobject()
    graph.set_points_smoothly([
        axes.coords_to_point(
            x, complex_to_real_func(y)/n_samples,
        )
        for x, y in zip(frequencies, fft_output[:n_samples//2])
    ])
    graph.set_color(color)
    f_min, f_max = [
        axes.x_axis.point_to_number(graph.get_points()[i])
        for i in (0, -1)
    ]
    graph.underlying_function = lambda f : axes.y_axis.point_to_number(
        graph.point_from_proportion((f - f_min)/(f_max - f_min))
    )
    return graph


def get_fourier_transform(
    func, t_min, t_max,
    complex_to_real_func = DEFAULT_COMPLEX_TO_REAL_FUNC,
    use_almost_fourier = USE_ALMOST_FOURIER_BY_DEFAULT,
    **kwargs ##Just eats these
    ):
    scalar = 1./(t_max - t_min) if use_almost_fourier else 1.0
    def fourier_transform(f):
        z = scalar*scipy.integrate.quad(
            lambda t : func(t)*np.exp(complex(0, -TAU*f*t)),
            t_min, t_max
        )[0]
        return complex_to_real_func(z)
    return fourier_transform



title = TexText("Fourier Transform")
title.scale(1.2)
title.to_edge(UP, buff = MED_SMALL_BUFF)

func = lambda t : np.cos(2*TAU*t) + np.cos(3*TAU*t)
# graph = ParametricCurve(func, t_range=(0, 5))

graph = FunctionGraph(func, x_range=(0, 5))
graph.stretch(0.25, 1)
graph.next_to(title, DOWN)
graph.to_edge(LEFT)
graph.set_color(BLUE)

fourier_graph = FunctionGraph(
    get_fourier_transform(func, 0, 5),
    (0, 5)
)

fourier_graph.move_to(graph)
fourier_graph.to_edge(RIGHT)
fourier_graph.set_color(RED)
arrow = Arrow(graph, fourier_graph, color=WHITE)
scene.play(*map(ShowCreation, (title, graph)))

# scene.student_thinks(
#     "What's that?",
#     look_at_arg = title,
#     target_mode = "confused",
#     student_index = 1,
# )
scene.play(
    GrowArrow(arrow),
    ReplacementTransform(graph.copy(), fourier_graph)
)
scene.wait(2)
# scene.student_thinks(
#     "Pssht, I got this",
#     target_mode = "tease",
#     student_index = 2,
#     added_anims = [RemovePiCreatureBubble(scene.students[1])]
# )
# scene.play(scene.teacher.change, "hesitant")
scene.hold_on()



