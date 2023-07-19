from operator import itemgetter

from my_utility_module import isclose
from point_module import Point
from vector_module import get_angle


class InternalBuilder:

    def __init__(self,shape):
        self.shape = shape
        self.shape_output = set()
        self.first = Point((0,0,0))

    def build_interior(self):
        spline_array = self.shape.get_spline_segment_array()

        for spline in spline_array:
            print("got spline", spline)
            for segment in spline:
                self.add_spline_from_segment(segment)


    def add_spline_from_segment(self, segment):
        previous = self.shape.get_point(segment[0])
        current = self.shape.get_point(segment[1])
        self.first = previous
        new_spline = [previous]
        counter = 0
        while current is not None and current!=self.first and counter<50:
            counter+=1
            new_spline.append(current)
            print("while",new_spline)
            potential_points = {self.shape.get_point(x) for x in self.shape.get_connected_points(current,True)}
            new_point = self.filter_clockwise(previous,current,potential_points)
            previous = current
            current = new_point
        self.shape_output.add(tuple(new_spline))

    def filter_clockwise(self, p, c, potential_points):
        filtered = [(x,get_angle(c,p,x)) for x in potential_points if x.distance(c)>1]
        #print("filt1",filtered)
        if len(filtered)>0:
            smallest_angle = min(filtered,key=itemgetter(1))
            #print("smallest",smallest_angle)
            filtered = [(x,x.distance(c)) for x,angle in filtered if isclose(angle, smallest_angle[1],abs_tol=1.01)]
            if len(filtered)>0:
                closest_point = min(filtered,key=itemgetter(1))[0]
                print("first",self.first,closest_point,self.first==closest_point)
                return closest_point
        print("returning None")
        return None
