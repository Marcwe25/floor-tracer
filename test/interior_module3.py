from collections import deque, defaultdict
from functools import partial
from math import fabs
from operator import itemgetter

from my_utility_module import isclose, get_from_set
from point_module import Point
from spline_module import SplinePath
from vector_module import get_angle, get_angle_of_vector
from timeit import default_timer as timer

class InternalBuilder:

    def __init__(self, shape):
        self.shape = shape
        self.shape_output = set()
        self.first = Point((0, 0, 0))
        self.segment_used = set()
        self.__xaxis = Point((1, 0, 0))
        self.t1 = 0
        self.t2 = 0
        self.t3 = 0
        self.t4 = 0
        self.t5 = 0
        self.t6 = 0
        self.t7 = 0
        self.t8 = 0
        self.n = 0

    def build_interior(self):
        spline_array = self.shape.get_spline_segment_array()

        for spline in spline_array:
            # print("got spline", spline)
            for segment in spline:
                if segment not in self.segment_used:
                    self.n += 1
                    self.add_spline_from_segment(segment)

        print("self.t1",self.t1)
        print("self.t2",self.t2)
        print("self.t3",self.t3)
        print("self.t4",self.t4)
        print("self.t5",self.t5)
        print("self.t6",self.t6)
        print("self.t7",self.t7)
        print("self.t8",self.t8)
        print("self.n",self.n)

    def add_spline_from_segment(self, segment):
        previous = self.shape.get_point(segment[0])
        current = self.shape.get_point(segment[1])
        first = self.shape.get_point(segment[0])
        new_spline = []
        counter = 0
        while current is not None and current != first and counter < 2000:
            #print("first",first)
            #print("fprevious",previous,"fcurrent",current)
            self.segment_used.add((previous, current))
            counter += 1
            #print("current", counter, current)
            new_spline.append(current)
            # print("while",new_spline)
            new_point = self.filter_segment_clockwise(previous, current, new_spline)

            # potential_points = {self.shape.get_point(x) for x in self.shape.get_connected_points(current, True)}
            # new_point = self.filter_clockwise(previous, current, potential_points)
            previous = current
            current = new_point
            #print("finished", counter)
        new_spline = [first]+new_spline
        self.shape_output.add(SplinePath(new_spline))
        #print("done", previous, current)

    def filter_clockwise(self, p, c, potential_points):
        filtered = [(x, get_angle(c, p, x)) for x in potential_points if x != c and x != p and x.distance(c) > 2]
        # print("filt1",filtered)
        if len(filtered) > 0:
            smallest_angle = min(filtered, key=itemgetter(1))
            # print("smallest",smallest_angle)
            filtered = [(x, x.distance(c)) for x, angle in filtered if isclose(angle, smallest_angle[1], abs_tol=1.01)]
            if len(filtered) > 0:
                closest_point = min(filtered, key=itemgetter(1))[0]
                print("returning ", self.first, closest_point, self.first == closest_point)
                return closest_point
        print("returning None")
        return None

    def filter_segment_clockwise(self, p, c, new_spline):

        timer1a = timer()
        segments = self.shape.get_facing_connected_segment(c)
        prev_segments = self.shape.get_prev_connected_segment(c,True)
        timer1b = timer()
        self.t1 += (timer1b-timer1a)

        p_angle = get_angle_of_vector( p-c,self.__xaxis)
        #print("p_angle",p_angle)

        timer2a = timer()
        prev_dict = {self.shape.get_point(segment_index[0]):segment_index for segment_index in prev_segments}
        facing_dict = {self.shape.get_point(segment_index[1]):segment_index for segment_index in segments}
        timer2b = timer()
        self.t2 += (timer2b-timer2a)

        #print("prev1 getting point      ",prev_dict)

        timer3a = timer()
        prev_dict = {prev_dict[k][0]:((self.shape.get_angle_for_index(prev_dict[k][0])+180)%360-p_angle+360)%360 for k in prev_dict if k not in new_spline}
        facing_dict = {facing_dict[k][1]:(self.shape.get_angle_for_index(facing_dict[k][0])-p_angle+360)%360 for k in facing_dict if k not in new_spline}
        timer3b = timer()
        self.t3 += (timer3b-timer3a)

        #print("prev2 removing previous  ",prev_dict)
        #print("faci1 getting point      ",facing_dict)
        #print("faci2 removing previous  ",facing_dict)

        timer4a = timer()
        for k in prev_dict:
            facing_dict[k] = prev_dict[k]
        timer4b = timer()
        self.t4 += (timer4b-timer4a)

        timer5a = timer()
        facing_dict = {k:facing_dict[k] for k in facing_dict if not isclose(facing_dict[k],0,abs_tol=3)}
        #print("uni removing returning   ",facing_dict)
        timer5b = timer()
        self.t5 += (timer5b-timer5a)


        if len(facing_dict)==0:
            return None

        timer6a = timer()
        smallest_angle = min(facing_dict,key=facing_dict.get)
        timer6b = timer()
        self.t6 += (timer6b-timer6a)

        timer7a = timer()
        #print("smallest angle           ",smallest_angle)
        facing_dict = {self.shape.get_point(k) for k in facing_dict if isclose(facing_dict[k],facing_dict[smallest_angle],abs_tol=1)}
        timer7b = timer()
        self.t7 += (timer7b-timer7a)

        #print("keeping smallest         ",facing_dict)

        timer8a = timer()
        if len(facing_dict)>1:
            facing_dict = {k:k.distance(c) for k in facing_dict}
            smallest_distance = min(facing_dict,key=facing_dict.get)
            #print("closest                  ",smallest_distance)
            timer8b = timer()
            self.t8 += (timer8b-timer8a)
            return smallest_distance
        else:
            timer8b = timer()
            self.t8 += (timer8b-timer8a)
            return get_from_set(facing_dict)
        # need point    remove duplicate
        # need point    remove segment with 0 length
        # need point    remove already used points (including prev and current)
        # need index (need angle)    remove segment returning through previous, that's the segment with angle 0
        # need index (need angle)    get the segment with smallest angle to previous

        return None

    def filter_segment_clockwise3(self, p, c, connected_segments):
        print("previous",p,"current",c)
        if len(connected_segments) == 2:
            segment = get_from_set(connected_segments)
            segment = {self.shape.get_point(x) for x in segment}.difference({p,c})
            point = get_from_set(segment)

            if segment[0] != segment[1]:
                if segment[0] == c:
                    return segment[1]
                else:
                    return segment[0]
        else:

            pcx_angle = get_angle_of_vector(self.__xaxis, c - p)
            filtered = [((self.shape.get_point(x[0]), self.shape.get_point(x[1])), (x[0],x[1])) for x in connected_segments]
            print("f1",filtered)
            filtered = [
                (
                    xpoint[0], fabs(180 - self.shape.get_angle_for_index(xindex[0]))
                ) if xpoint[1] == c else (
                    xpoint[1], self.shape.get_angle_for_index(xindex[0])
                ) for xpoint, xindex in filtered if xpoint[0] != xpoint[1]]
            print("f2",filtered)
            filtered = [(x, angle) for x, angle in filtered if not isclose(angle,pcx_angle,abs_tol=3)]
            if len(filtered) == 1:
                if filtered[0][0] == c:
                    return filtered[0][1]
                else:
                    return filtered[0][0]
            filtered = [(x, angle - pcx_angle) if angle > pcx_angle else (x, 360 + angle - pcx_angle) for x, angle in
                        filtered]
            print("f3",filtered)
            smallest_angle = min(filtered, key=itemgetter(1))
            # print("smallest",smallest_angle)
            filtered = [x for x, angle in filtered if isclose(angle, smallest_angle[1], abs_tol=1.01)]
            print("f4",filtered)

            if len(filtered) == 1:
                return filtered[0]
            filtered = [(x, x.distance(c)) for x in filtered]
            closest_point = min(filtered, key=itemgetter(1))[0]
            # print("returning ",self.first,closest_point,self.first==closest_point)
            return closest_point
        # print("returning None")
        return None

    def filter_segment_clockwise2(self, p, c, connected_segments):
        if len(connected_segments) == 1:
            segment = get_from_set(connected_segments)
            if segment[0] != segment[1]:
                if segment[0] == c:
                    return self.shape.get_point(segment[1])
                else:
                    return self.shape.get_point(segment[0])
        else:
            pcx_angle = get_angle_of_vector(self.__xaxis, c - p)
            map(partial(self.m_1, mc=c), connected_segments)
            connected_segments = [(x, angle) for x, angle in connected_segments if angle != pcx_angle]
            if len(connected_segments) == 1:
                if connected_segments[0][0] == c:
                    return connected_segments[0][1]
                else:
                    return connected_segments[0][0]
            print("c1", connected_segments)
            map(partial(self.m_2, mpcx_angle=pcx_angle), connected_segments)

            smallest_angle = min(connected_segments, key=itemgetter(1))
            # print("smallest",smallest_angle)
            connected_segments = [x for x, angle in connected_segments if
                                  isclose(angle, smallest_angle[1], abs_tol=1.01)]
            if len(connected_segments) == 1:
                return connected_segments[0]

            map(partial(self.m_3, mc=c), connected_segments)
            closest_point = min(connected_segments, key=itemgetter(1))[0]
            # print("returning ",self.first,closest_point,self.first==closest_point)
            return closest_point
        # print("returning None")
        return None

    def get_output(self):
        output = deque()
        for spline_class in self.shape_output:
            output.append(spline_class.spline_list)
        return output

    def m_1(self, x, mc):
        if x[1] == mc:
            return self.shape.get_point(x[0]), fabs(180 - self.shape.get_angle_for_index(x[0]))
        else:
            return self.shape.get_point(x[1]), self.shape.get_angle_for_index(x[0])

    def m_2(self, x, mpcx_angle):
        if x[1] > mpcx_angle:
            return x[0], x[1] - mpcx_angle
        else:
            return x[0], 360 + x[1] - mpcx_angle

    def m_3(self, x, mc):
        return x, mc.distance(x)
