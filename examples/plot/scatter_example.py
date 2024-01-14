from examples.example_imports import *

class ScatterExample(EagerModeScene):

    def clip1(self):
        n_features = 2
        X = np.random.normal(0, 20, (2000, n_features))
        theta = np.linspace(0, np.pi*2, 150)
        r = 50
        x, y = r*np.cos(theta), r*np.sin(theta)
        self.scatter2d(X[:, 0], X[:, 1], size=.03, color=YELLOW)
        self.scatter2d(x, y, size=.03, color=BLUE)

    def clip_2(self):
        x1, y1 = np.random.randn(2, 200)
        x2, y2 = np.random.randn(2, 200)
        self.scatter2d(x1, y1, size=.05, color=BLUE, x_range=(-3, 3), y_range=(-3, 3))
        self.scatter2d(x2, y2, size=.05, color=YELLOW)

ScatterExample().render()
