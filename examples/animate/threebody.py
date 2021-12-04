from examples.example_imports import *

G = 5


def get_a(obja, objs, masses):
    acc = 0
    for i, j in zip(objs, masses):
        acc += G * j / get_norm(i - obja) ** (2) * normalize(i - obja)
    return acc


class simulation(EagerModeScene):
    def clip0(self):
        frame = self.camera.frame
        frame.set_euler_angles(
            theta=-30 * DEGREES,
            phi=70 * DEGREES,
        )
        frame.add_updater(lambda obj, dt: obj.increment_theta(-0.1 * dt))
        self.add(frame)

        vg = Group(
            Sphere(radius=0.1, color=RED),
            Sphere(radius=0.2, color=GREEN),
            Sphere(radius=0.15, color=BLUE)
        )
        self.a = np.array([np.array([0, 0, 0]), np.array([0, 0, 0]), np.array([0, 0, 0])])
        self.v = np.array([np.array([1, 0, 1]), np.array([0, -1, 0]), np.array([-1, 1, -1])])
        self.x = np.array([np.array([1, 2, 1]), np.array([-2, -2, 1]), np.array([1, 1, 0.5])])
        m = [1, 1, 1]

        for ball, x in zip(vg, self.x):
            ball.move_to(x)

        def update(obj, dt):
            for g in range(10):
                self.a = np.array([get_a(self.x[i], [*self.x[:i], *self.x[i + 1:]], m) for i in range(len(self.x))])
                self.v = self.v + self.a * dt / 10
                self.x = self.x + self.v * dt / 10
            for ball, x in zip(obj, self.x):
                ball.move_to(x)

        trace = VGroup(
            *[TracedPath(ball.get_center, min_distance_to_new_point=0.01).set_color(color) for ball, color in
              zip(vg, [RED, GREEN, BLUE])]
        )

        vg.add_updater(update)
        self.add(vg, trace)
        self.wait(100)

simulation().render()