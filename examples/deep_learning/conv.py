import numpy as np

from examples.example_imports import *
import scipy.stats as st


def box_blur(n):
    return np.ones((n, n)) / (n ** 2)


def gaussion_kernel(kernlen=3, nsig=3):
    x = np.linspace(-nsig, nsig, kernlen + 1)
    kern1d = np.diff(st.norm.cdf(x))
    kern2d = np.outer(kern1d, kern1d)
    return kern2d / kern2d.sum()


class ConvScene(EagerModeScene):
    def __init__(self):
        super().__init__()
        self.init()

    def init(self):
        image = Image.open(get_full_raster_image_path("pic2"))
        size = 30
        image = image.resize([size, size])
        start = 0
        delta_x = -1  # 30
        delta_y = -1  # 30
        end_x = start + delta_x
        end_y = start + delta_y
        arr = np.asarray(image)[start:end_x, start:end_y, :]
        height, width = arr.shape[:2]
        self.height, self.width = height, width
        pixel_array = VGroup(*[
            Circle(fill_color=rgb_to_hex(arr[i, j] / 255), fill_opacity=1)
            for i in range(height)
            for j in range(width)
        ])

        pixel_array.arrange_in_grid(height, width, buff=0)
        pixel_array.set_height(6)
        pixel_array.set_stroke(WHITE, 1, opacity=0)
        pixel_array.to_edge(LEFT, buff=LARGE_BUFF)
        new_array = pixel_array.copy()
        new_array.next_to(pixel_array, RIGHT, buff=2)
        new_array.set_fill(BLACK, 0)
        self.pixel_array = pixel_array
        self.new_array = new_array

    def clip1(self):
        frame = self.camera.frame
        self.play(ShowCreation(self.pixel_array), run_time=2)
        self.play(Write(self.new_array))
        new_array = self.new_array
        pixel_array = self.pixel_array

        def get_kernel_array(kernel):
            kernel_array = VGroup()
            for row in kernel:
                for x in row:
                    square = self.pixel_array[0].copy()
                    square.set_fill(BLACK, 0)
                    square.set_stroke(BLUE, 2)
                    value = DecimalNumber(x, num_decimal_places=3)
                    value.set_width(square.get_width() * 0.7)
                    value.set_stroke(BLACK, 1, background=True)
                    value.move_to(square)
                    square.add(value)
                    kernel_array.add(square)
            kernel_array.arrange_in_grid(*kernel.shape, buff=0)
            kernel_array.move_to(self.pixel_array[0])
            return kernel_array

        kernel = box_blur(5)
        kernel_array = get_kernel_array(kernel=kernel)
        self.add(kernel_array)

        right_rect = new_array[0].copy()
        right_rect.set_stroke(BLUE, 2)
        self.add(right_rect)

        width = self.width
        height = self.height

        def step(pos=0):
            i = pos // width
            j = pos % width

            h, w = kernel.shape
            pixels = np.array([
                square.data["fill_rgba"][0]
                for square in pixel_array
            ]).reshape((height, width, 4))

            rgba = sum([
                kernel[k, l] * pixels[i - k, j - l]
                for k in range(-(w // 2), w // 2 + 1)
                for l in range(-(h // 2), h // 2 + 1)
                if (0 <= i - k < pixels.shape[0]) and (0 <= j - l < pixels.shape[1])
            ])

            kernel_array.move_to(pixel_array[pos])
            right_rect.move_to(new_array[pos])
            new_array[pos].data["fill_rgba"][0] = rgba

        def walk(start, stop, time=5, surface=None, kernel_array=kernel_array):
            print(f"stop-start={stop - start}")
            for n in range(start, stop):
                step(n)
                if surface is not None:
                    surface.move_to(kernel_array, IN)
                self.wait(time / (stop - start))

        # Setup zooming
        def zoom_to_kernel():
            self.play(
                frame.set_height, 1.5 * kernel_array.get_height(),
                frame.move_to, kernel_array,
                run_time=2
            )

        def zoom_to_new_pixel():
            self.play(
                frame.set_height, 1.5 * kernel_array.get_height(),
                frame.move_to, right_rect,
                run_time=2
            )

        def reset_frame():
            self.play(
                frame.to_default_state
            )

        # Example walking
        # walk(0, 151, 15)
        last_i = 0
        next_i = 50
        walk(last_i, next_i, 5)
        self.wait()
        zoom_to_kernel()
        self.wait()
        reset_frame()
        zoom_to_new_pixel()
        self.wait()
        reset_frame()

        # Gauss surface
        gaussian = ParametricSurface(
            lambda u, v: [u, v, np.exp(-(u ** 2) - v ** 2)],
            u_range=(-3, 3),
            v_range=(-3, 3),
            resolution=(101, 101),
        )
        gaussian.set_color(BLUE, 0.8)
        gaussian.match_width(kernel_array)
        gaussian.stretch(2, 2)

        self.play(FadeOut(kernel_array))
        gausskernel = gaussion_kernel(5, 3)
        kernel_array = get_kernel_array(kernel=gausskernel)
        self.play(FadeIn(kernel_array))
        gaussian.move_to(kernel_array, IN)
        self.play(
            FadeIn(gaussian),
            frame.set_phi, 70 * DEGREES,
            frame.set_theta, 10 * DEGREES,
            run_time=3
        )
        self.wait()
        self.play(
            frame.set_height, 8,
            frame.set_theta, 0,
            frame.set_x, 0,
            run_time=3,
        )

        # More walking
        walk(0, len(pixel_array), time=10, surface=gaussian, kernel_array=kernel_array)
        self.wait()
        self.play(frame.to_default_state, run_time=2)
        self.wait()

        # self.file_writer.finish()


CONFIG.preview = True
ConvScene().render()
