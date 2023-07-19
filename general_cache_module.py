from point_module import Point
from vector_module import get_angle_of_vector


class GeneralCache:

    def __init__(self,user_function, param):
        self.return_value = None
        self.user_function = user_function
        self.param = param

    def get_return_value(self):
        self.return_value = self.user_function(self.param)
        self.get_return_value = self.cached_value
        return self.return_value

    def cached_value(self):
        return self.return_value

class AngleCache:

    xaxis = Point((1, 0, 0))
    shape = None

    def __init__(self, point_from_index, point_to_index):
        self.return_value = None
        self.point_from_index = point_from_index
        self.point_to_index = point_to_index

    def get_angle(self):
        self.return_value = self.angle_function()
        self.get_angle = self.cached_value
        return self.return_value

    def cached_value(self):
        return self.return_value

    def angle_function(self):
        return get_angle_of_vector(AngleCache.shape.get_point(self.point_to_index)-AngleCache.shape.get_point(self.point_from_index), AngleCache.xaxis)
