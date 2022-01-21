from examples.example_imports import *
import scipy.integrate as integrate

CONFIG.preview = True
class DouPandulumSim:
    def __init__(self, th1, th2):
        self.x1, self.x2, self.y1, self.y2 = DouPandulumSim.getSimulationResult(th1, th2)

    @staticmethod
    def derivs(state, t):
        G = 9.8  # acceleration due to gravity, in m/s^2
        L1 = 1.0  # length of pendulum 1 in m
        L2 = 1.0  # length of pendulum 2 in m
        M1 = 1.0  # mass of pendulum 1 in kg
        M2 = 1.0  # mass of pendulum 2 in kg
        dydx = np.zeros_like(state)
        dydx[0] = state[1]

        delta = state[2] - state[0]
        den1 = (M1 + M2) * L1 - M2 * L1 * np.cos(delta) * np.cos(delta)
        dydx[1] = ((M2 * L1 * state[1] * state[1] * np.sin(delta) * np.cos(delta)
                    + M2 * G * np.sin(state[2]) * np.cos(delta)
                    + M2 * L2 * state[3] * state[3] * np.sin(delta)
                    - (M1 + M2) * G * np.sin(state[0]))
                   / den1)

        dydx[2] = state[3]

        den2 = (L2 / L1) * den1
        dydx[3] = ((- M2 * L2 * state[3] * state[3] * np.sin(delta) * np.cos(delta)
                    + (M1 + M2) * G * np.sin(state[0]) * np.cos(delta)
                    - (M1 + M2) * L1 * state[1] * state[1] * np.sin(delta)
                    - (M1 + M2) * G * np.sin(state[2]))
                   / den2)

        return dydx

    @staticmethod
    def getSimulationResult(th1, th2):
        G = 9.8  # acceleration due to gravity, in m/s^2
        L1 = 1.0  # length of pendulum 1 in m
        L2 = 1.0  # length of pendulum 2 in m
        M1 = 1.0  # mass of pendulum 1 in kg
        M2 = 1.0  # mass of pendulum 2 in kg
        # create a time array from 0..100 sampled at 0.05 second steps
        dt = 0.01
        t = np.arange(0, 21, dt)

        # th1 and th2 are the initial angles (degrees)
        # w10 and w20 are the initial angular velocities (degrees per second)
        # th1 = 120.0
        w1 = 0.0
        # th2 = -10.0
        w2 = 0.0

        # initial state
        state = np.radians([th1, w1, th2, w2])

        # integrate your ODE unp.sing scipy.integrate.
        y = integrate.odeint(DouPandulumSim.derivs, state, t)

        x1 = L1 * np.sin(y[:, 0])
        y1 = -L1 * np.cos(y[:, 0])

        x2 = L2 * np.sin(y[:, 2]) + x1
        y2 = -L2 * np.cos(y[:, 2]) + y1

        return x1, x2, y1, y2


class DouPandulumLine(VGroup):
    CONFIG = {}

    def __init__(self, line1, line2, **kwargs):
        line1.set_color(RED)
        line2.set_color(BLUE)
        VGroup.__init__(
            self, line1, line2
        )

    def resetLines(self, line1, line2):
        newState = DouPandulumLine(line1, line2)
        self = self.become(newState)


scene = EagerModeScene()
plane = NumberPlane(x_range=(-7, 7), y_range=(-4, 4))
plane.add_coordinate_labels()

scene.play(Write(plane))

douPandulumSimulator = DouPandulumSim(120., -10.)
def getLinesFromTick(ts):
    x1 = douPandulumSimulator.x1[ts]
    x2 = douPandulumSimulator.x2[ts]
    y1 = douPandulumSimulator.y1[ts]
    y2 = douPandulumSimulator.y2[ts]
    line1 = Line(np.array((0., 0., 0.)), np.array((x1, y1, 0.)))
    line2 = Line(np.array((x1, y1, 0.)), np.array((x2, y2, 0.)))
    return line1, line2

line1, line2 = getLinesFromTick(0)
doupandulumLine = DouPandulumLine(line1, line2)
scene.add(doupandulumLine)
dot = Dot()
dot.move_to(np.array((-1., -5., 0.)))


def update_pandulum(obj):
    center = dot.get_center()
    xPos = center[0]
    ts = int(np.floor((1.0 + xPos) / 0.002))
    line1, line2 = getLinesFromTick(ts)
    obj.resetLines(line1, line2)


doupandulumLine.add_updater(update_pandulum)
scene.add(doupandulumLine)
dot.move_to(LEFT + DOWN)
scene.play(dot.move_to, RIGHT + DOWN, rate_func=linear, run_time=5)

scene.hold_on()
