

# Install

```bash
pip install manim_express
```

The above steps will automatically install packages `manim_express` and  `manimlib`(my fork version) for you. Then you can code with them anywhere.  



# Quick start

* Render an animation: [SquareToCircle](https://3b1b.github.io/manim/getting_started/quickstart.html#add-animations)

  ```python
  from manimlib import *
  from manim_express import EagerModeScene
  
  scene = EagerModeScene()
  circle = Circle()
  circle.set_fill(BLUE, opacity=0.5)
  circle.set_stroke(BLUE_E, width=4)
  
  square = Square()
  scene.play(ShowCreation(square))
  scene.play(ReplacementTransform(square, circle))
  
  scene.hold_on()
  ```
  
  

* `manim_express` vs `Matplotlib`:

  ```python
  from manimlib import *
  from manim_express import EagerModeScene
  import numpy as np
  
  x = np.linspace(0, 2*np.pi, 100)
  y = np.sin(5*x)
  
  # matplotlib
  import matplotlib.pyplot as plt
  
  plt.plot(x, y, color='green', linewidth=2)
  plt.show()
  
  # manim_express
  from manim_express.plot import m_line, m_scatter
  scene = EagerModeScene()
  
  line = m_line(x, y, color=GREEN, width=2)
  scene.add(line)
  scene.hold_on()
  ```

  





# Resources

* Wiki  
  
  https://3b1b.github.io/manim/
  
  https://manim.wiki/  
  https://manim.wiki/shaders/
  
* 3B1B videos:  
  https://github.com/3b1b/videos





# Examples
* GOA model
  <img src="data/pic/GOA.PNG" width = "900"/>