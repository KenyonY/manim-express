

# Install

```bash
pip install manim_express
```

The above steps will automatically install packages `manim_express` and  `manimlib`(my fork version) for you. Then you can code with them anywhere.  



# Quick start

* Render an animation: [SquareToCircle](https://3b1b.github.io/manim/getting_started/quickstart.html#add-animations)

  ```python
  from manim_express import EagerModeScene
  from manimlib import *
  
  scene = EagerModeScene()
  circle = Circle()
  circle.set_fill(BLUE, opacity=0.5)
  circle.set_stroke(BLUE_E, width=4)
  
  square = Square()
  
  scene.play(ShowCreation(square))
  
  scene.play(ReplacementTransform(square, circle))
  
  scene.hold_on()
  ```

  





# Resources

* Chinese Wiki  
  https://manim.wiki/  
  https://manim.wiki/shaders/
* 3B1B videos:  
  https://github.com/3b1b/videos





# Examples
* GOA model
  <img src="data/pic/GOA.PNG" width = "900"/>