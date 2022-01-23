from examples.example_imports import *
import imageio


class Animations(EagerModeScene):
    def __init__(self):
        super(Animations, self).__init__()

    # def clip7(self):
    #     pass

    def clip8(self):
        theta = np.linspace(0, 2 * PI, 50)
        x = np.cos(theta)
        y = np.sin(theta)
        points = xyz_to_points(x, y)
        dc = DotCloud(points, color=GREEN_C)
        self.add(dc)
        import cv2
        # image = imageio.imread("../../data/pic/code0.png")

        image = imageio.imread("../../data/pic/USST_logo.svg.png")
        # image = cv2.resize(image, (128, 128))

        arr = np.array(image) / 255
        image_obj = image_arr_obj(arr, style=0)

        self.add(image_obj)

        # self.camera.frame.

    def clip9(self):
        arr = np.random.rand(10, 10, 3) * 255

        image = imageio.imread("../../data/pic/code0.png")
        # pixel_array = imobj(image[200:250, :250, :])
        pixel_array = imobj_square(arr)

        pixel_array.to_edge(LEFT, buff=LARGE_BUFF)

        new_array = pixel_array.copy()
        new_array.next_to(pixel_array, RIGHT, buff=2)
        new_array.set_fill(BLACK, 0)

        self.add(pixel_array)
        self.add(new_array)

        tri = Triangle()

        self.add(tri)
        self.hold_on()


Animations().clip9()
