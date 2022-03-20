# manim_express
[![image](https://img.shields.io/badge/Pypi-0.6.7-green.svg)](https://pypi.org/project/manim_express)
[![image](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/)
[![image](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![image](https://img.shields.io/badge/author-kunyuan-orange.svg?style=flat-square&logo=appveyor)](https://github.com/beidongjiedeguang)


------------------------
[**English**](https://github.com/beidongjiedeguang/manim-express/blob/dev/README.md) |
[**中文说明**](https://github.com/beidongjiedeguang/manim-express/blob/dev/README_zh.md) 

## Install

```bash
pip install manim_express
```

以上步骤将安装 `manim_express` 和  [`manimlib`](https://github.com/beidongjiedeguang/manimlib). 然后就可以在任何代码位置导入使用这个动画库了.  


## 快速开始

* 渲染一个动画: [3b1b:SquareToCircle](https://3b1b.github.io/manim/getting_started/quickstart.html#add-animations)

  ```python
  from manimlib import *
  from manim_express import GlEagerScene
  
  scene = GlEagerScene()
  circle = Circle()
  circle.set_fill(BLUE, opacity=0.5)
  circle.set_stroke(BLUE_E, width=4)
  
  square = Square()
  scene.play(ShowCreation(square))
  scene.play(ReplacementTransform(square, circle))
  
  scene.hold_on()
  ```
  
  与渲染画面交互:
  * 按住 `d` 键 或 **鼠标左键** 然后移动鼠标可以改变三维空间中相机的旋转视角.
  * 按住 `s` 键 或 **鼠标右键** 然后移动鼠标可以平移相机. 
  * 按住 `z` 键 或 **ctrl键** 同时滚动鼠标滚轮以缩放画面. 
  * 通过 `r` 重制相机视角.
  * 离开/退出当前动画: `q` or `tab`
  * 暂停动画:  `space` or `ctrl` or `alt`
  * 前一段动画: `LEFT`
  * 后一段动画: `RIGHT`
  * 重新播放当前动画: `DOWN`
  
* `manim_express` vs `Matplotlib`:  
  **使用Eager mode**:
  ```python
  from manimlib import *
  from manim_express import GlEagerScene
  CONFIG.use_online_tex = True # If you don't have installed latex locally.
  theta = np.linspace(0, 2*np.pi, 200)
  x = np.cos(theta)
  y = np.sin(theta)
  
  scene = GlEagerScene()
  scene.plot(x, y, color=GREEN, width=2, scale_ratio=1)
  scene.hold_on()
  ```
  **使用面向对象的方式**:

  ```python
  from manimlib import *
  from manim_express import GlEagerScene
  from sklearn.datasets import make_multilabel_classification 
  class ScatterExample(GlEagerScene):
      def clip_1(self):
          X1, y1 =make_multilabel_classification(n_samples=200, n_classes=4, n_features=2)
          X2, y2 =make_multilabel_classification(n_samples=200, n_classes=4, n_features=2)
          self.scatter2d(X1[:, 0], X1[:, 1], size=.05, color=BLUE)
          self.scatter2d(X2[:, 0], X2[:, 1], size=.05, color=YELLOW)
  
  ScatterExample().render()
  ```
  <img src="data/pic/scatter.png" width = "600"/>
  但是需要注意，manim并不适合绘制需要精确实现的图案！
  
  
  
  



# 资源

* Wiki  
  https://flyingframes.readthedocs.io/en/latest/index.html  
  https://3b1b.github.io/manim/  
  https://docs.manim.org.cn/  
  https://docs.manim.org.cn/shaders/
  
* 3B1B videos:  
  https://github.com/3b1b/videos

* export pptx
  * https://github.com/yoshiask/manim-pptx
  * https://github.com/RythenGlyth/manim-pptx
  * https://manimcommunity.github.io/manim_editor/Tutorial/index.html


# Examples

- Bezier curve  
 
  https://user-images.githubusercontent.com/32060638/159116579-083692a2-f12c-48c0-8abd-1ee147e63714.mp4

 
- GOA model

  https://user-images.githubusercontent.com/32060638/159116901-eafa5842-135c-47f5-85a8-c946099a160f.mp4

- GOA  
  <img src="data/pic/GOA.PNG" width = "600"/>

- Apply function  
  <img src="data/pic/apply_function.gif" width = "600"/>


- Double pendulum  
  <img src="data/pic/pendulum.gif" width = "600"/>
