from operator import itemgetter

from my_utility_module import isclose
from vector_module import get_angle


class InternalBuilder:

    def __init__(self,shape):
        self.shape = shape
        self.shap_output = set()

    def build_internal(self):
        spline_array = self.shape.get_spline_segment_array()
        for spline in spline_array:
            for segment in spline:
                self.add_spline_from_segment(segment)

    def add_spline_from_segment(self,segment):
        previous = self.shape.get_point(segment[0])
        current = self.shape.get_point(segment[1])
        first = self.shape.get_point(segment[0])
        new_spline = [segment[0],segment[1]]
        while current is not None and current!=first:
            print("while")
            new_spline.append((current))
            potential_next_points = {self.shape.get_point(x) for x in self.shape.get_connected_points(current,False)}
            potential_next_points.difference_update(new_spline)
            print("previous",previous)
            print("current",current)
            print("potential_next_points",potential_next_points)
            new_point = self.filter_clockwise(previous,current,potential_next_points)
            previous = current
            current = new_point
        self.shap_output.add(tuple(new_spline))

    def filter_clockwise(self,p,c,potential_next_points):
        print("c",c)
        print("p",p)
        print("points",potential_next_points)
        filtered = [(x,get_angle(c,p,x)) for x in potential_next_points]
        if len(filtered)>0:
            smallest_angle = min(filtered,key=itemgetter(1))
            filtered = [(x,x.distance(c)) for x,angle in filtered if isclose(angle,smallest_angle[1],abs_tol=1)]
            if len(filtered)>0:
                closest_point = min(filtered,key=itemgetter(1))
                return closest_point
        return None
