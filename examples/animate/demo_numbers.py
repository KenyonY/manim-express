import numpy as np

from examples.example_imports import *

scene = EagerModeScene()
scene.save_default_config()
number = DecimalNumber(0).scale(2)
scene.add(number)
scene.wait()
print(np.linspace(0, 10, 4))
scene.play(ChangingDecimal(number, lambda x: x*10), run_time=4)



scene.hold_on()
