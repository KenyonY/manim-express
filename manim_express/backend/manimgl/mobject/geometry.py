from manimlib.mobject.geometry import *


class ModifiedArc(Arc):
    def get_start_angle(self):
        # Fixed dimension error
        angle = angle_of_vector(self.get_start() - self.get_arc_center().reshape(3))
        return angle % TAU


Arc.get_start_angle = ModifiedArc.get_start_angle
