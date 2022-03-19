from examples.example_imports import *


class ScatterExample(EagerModeScene):
    def clip1(self):
        X1, y1 = datasets.make_multilabel_classification(
            n_samples=200, n_classes=4, n_features=2, random_state=1
        )
        X1: np.ndarray
        # self.scatter2d(X1[:, 0], X1[:, 1], size=.05)
        self.plot(X1[:, 0], X1[:, 1], )
        self.show_plot()


ScatterExample().render()
