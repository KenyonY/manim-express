from examples.example_imports import *
# SceneArgs.color = "#ffffff"
scene = EagerModeScene()
code = """
import numpy as np
import matplotlib.pyplot as plt
theta = np.linspace(0, 2*np.pi, 1000)
x = np.cos(theta)
y = np.sin(theta)
plt.plot(x, y)
plt.show()
"""
code_obj = Code(code, )

scene.play(ShowCreation(code_obj))
scene.play(Transform(code_obj, code_obj.copy().scale(3)))
scene.hold_on()
