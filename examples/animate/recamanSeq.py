from examples.example_imports import *

VIOLET = "#EE82EE"
INDIGO = "#4B0082"
VIBGYOR = [VIOLET, INDIGO, BLUE, GREEN, YELLOW, ORANGE, RED]


class RecamanSequence(EagerModeScene):
    CONFIG = {
        "n": 100,  # number of iterations
    }

    def clip1(self):
        self.count = 0
        visited = [0] + [None] * self.n
        arcs = VGroup()

        self.index = 0  # acts as a pointer
        self.highest = max(self.index, 3)  # use to define the frame width

        for i in range(self.n):
            index = self.index - self.count

            if index < 0 or index in visited:
                index = self.index + self.count

            # defining the start and end of the arc
            start = np.array([visited[self.count], 0, 0])
            end = np.array([index, 0, 0])

            # defining the angle of arc (i.e., upwards arc or downwards arc)
            angle = -PI if self.count % 2 == 0 else PI

            if index < visited[self.count]:
                angle *= -1

            arc = ArcBetweenPoints(start, end, angle)
            arcs.add(arc)

            # updating variables
            self.index = index
            self.count += 1
            visited[self.count] = self.index

        VIBGYOR.reverse()

        arcs.set_color_by_gradient(*VIBGYOR)

        # rendering
        for i, arc in enumerate(arcs):
            self.highest = max(self.highest, max(visited[:i + 2]))
            arc.set_stroke(opacity=1 - (np.sqrt(i) / self.n))

            self.play(
                ShowCreation(arc),
                self.camera.frame.set_width, self.highest,
                self.camera.frame.move_to, self.highest / 2 * RIGHT,
                rate_func=linear,
                run_time=0.25
            )


if __name__ == "__main__":
    import os

    RecamanSequence().render()
