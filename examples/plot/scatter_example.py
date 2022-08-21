import numpy as np

from examples.example_imports import *


class ScatterExample(EagerModeScene):
    def get_X(self, n_features=2):
        X, y = datasets.make_multilabel_classification(
            n_samples=200, n_classes=4, n_features=n_features,
        )
        return X, y

    def clip1(self):
        X1, y1 = self.get_X()
        X2, y2 = self.get_X()
        self.scatter2d(X2[:, 0], X2[:, 1], size=.03, color=YELLOW)
        self.scatter2d(X1[:, 0], X1[:, 1], size=.03)

    def clip2(self):
        size = 0.05
        color = BLUE

        X, y = self.get_X(n_features=3)
        X: np.ndarray
        print(X.shape)
        x, y, z = X[:, 0], X[:, 1], X[:, 2]
        self.scatter3d(x, y, z, color=YELLOW)



ScatterExample().render()
