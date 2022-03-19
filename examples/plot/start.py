from examples.example_imports import *
from sklearn import datasets


# CONFIG.use_online_tex = True


class PlotScene(EagerModeScene):
    def clip1(self):
        X1, y1 = datasets.make_multilabel_classification(
            n_samples=200, n_classes=4, n_features=2, random_state=1
        )

        theta = np.linspace(0, TAU, 100)

        x = np.cos(theta)
        y = np.sin(theta)

        self.plot(X1[:,0], X1[:,1],
                  x_label='t', y_label='f(t)',
                  # scale_ratio=1,
                  )

        self.show_plot()
        self.hold_on()


PlotScene().render()
