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

    def __init__(self, shape,contour):
        shape.rebuild_all_index()
        self.shape = shape
        self.shape_output = set()
        self.contour=SplinePath(contour)
        self.shape_output.add(self.contour)
        self.first = Point((0, 0, 0))
        self.spline_array = None
        self.get_seg = None
        self.pre_seg = None

        self.segment_used = set()

        self.s2y = partial(defaultdict, set)
        self.s2x = partial(defaultdict, self.s2y)
        self.s1y = partial(defaultdict, self.s2x)
        self.s1x = defaultdict(self.s1y)

        self.s3y = partial(defaultdict, set)
        self.s3x = defaultdict(self.s3y)

        self.__xaxis = Point((1, 0, 0))

        self.t0 = 0
        self.t1_1 = 0
        self.t1_2 = 0
        self.t2 = 0
        self.t3 = 0
        self.t4 = 0
        self.t5 = 0
        self.t6 = 0
        self.t7 = 0
        self.t8 = 0
        self.t9 = 0
        self.t94 = 0
        self.t93 = 0
        self.t92 = 0
        self.t91 = 0
        self.t10 = 0
        self.t11 = 0
        self.t12 = 0
        self.t13 = 0
        self.n = 0
        self.f = 0

    def build_interior(self):
        timer0a = timer()
        self.spline_array = self.shape.segment_array
        timer0b = timer()
        self.t0 += (timer0b - timer0a)
        for spline in self.spline_array:
            # print("got spline", spline)
            for segment in spline:
                # if segment not in self.segment_used:
                if not self.already_use((self.shape.get_point(segment[0]), self.shape.get_point(segment[1]))):
                    self.n += 1
                    timer12a = timer()
                    self.add_spline_from_segment(segment)
                    timer12b = timer()
                    self.t12 += (timer12b - timer12a)
        self.shape_output.remove(self.contour)
        #print("self.t0", self.t0)
        #print("self.t1_1", self.t1_1)
        #print("self.t1_2", self.t1_2)
        #print("self.t2", self.t2)
        #print("self.t3", self.t3)
        #print("self.t4", self.t4)
        #print("self.t5", self.t5)
        #print("self.t6", self.t6)
        #print("self.t7", self.t7)
        #print("self.t8", self.t8)
        #print("self.t91", self.t91)
        #print("self.t92", self.t92)
        #print("self.t93", self.t93)
        #print("self.t94", self.t94)

        #print("self.t10", self.t10)
        #print("self.t11", self.t11)
        #print("self.t12", self.t12)
        #print("self.t13", self.t13)
        #print("self.n", self.n)
        #print("self.f", self.f)

    def add_spline_from_segment(self, segment):

        timer11a = timer()
        previous = self.shape.get_point(segment[0])
        current = self.shape.get_point(segment[1])
        first = self.shape.get_point(segment[0])
        timer11b = timer()

        new_spline = []
        counter = 0
        self.t11 += (timer11b - timer11a)
        while current is not None and current != first and counter < 2000:
            timer91a = timer()
            # print("first",first)
            # print("fprevious",previous,"fcurrent",current)
            # self.segment_used.add((previous, current))
            self.add_to_used((previous, current))
            timer91b = timer()
            self.t91 += (timer91b - timer91a)

            counter += 1

            timer92a = timer()
            # print("current", counter, current)
            new_spline.append(current)
            # print("while",new_spline)
            timer92b = timer()
            self.t92 += (timer92b - timer92a)

            timer93a = timer()
            new_point = self.filter_segment_clockwise(previous, current, new_spline)
            timer93b = timer()
            self.t93 += (timer93b - timer93a)

            timer94a = timer()
            previous = current
            current = new_point
            timer94b = timer()
            self.t94 += (timer94b - timer94a)
            # print("finished", counter)

        timer13a = timer()
        new_spline = [first] + new_spline
        timer13b = timer()
        self.t13 += (timer13b - timer13a)

        timer10a = timer()
        self.shape_output.add(SplinePath(new_spline))
        timer10b = timer()
        self.t10 += (timer10b - timer10a)

        # print("done", previous, current)

    def filter_segment_clockwise(self, p, c, new_spline):
        self.f += 1
        timer1_1a = timer()
        #segments = self.shape.get_facing_connected_segment(c)
        segments = self.shape.get_seg_from_index(c)
        timer1_1b = timer()
        self.t1_1 += (timer1_1b - timer1_1a)

        timer1_2a = timer()
        #prev_segments = self.shape.get_prev_connected_segment(c, True)
        prev_segments = self.shape.pre_seg_from_index(c)
        timer1_2b = timer()
        self.t1_2 += (timer1_2b - timer1_2a)

        p_angle = get_angle_of_vector(p - c, self.__xaxis)
        # print("p_angle",p_angle)

        timer2a = timer()
        prev_dict = {self.shape.get_point(segment_index[0]): segment_index for segment_index in prev_segments}
        facing_dict = {self.shape.get_point(segment_index[1]): segment_index for segment_index in segments}
        timer2b = timer()
        self.t2 += (timer2b - timer2a)

        # print("prev1 getting point      ",prev_dict)

        timer3a = timer()
        prev_dict = {prev_dict[k][0]: self.m1(p_angle, prev_dict[k][0]) for k in prev_dict if k not in new_spline}
        facing_dict = {facing_dict[k][1]: self.m2(p_angle, facing_dict[k][0]) for k in facing_dict if
                       k not in new_spline}

        timer3b = timer()
        self.t3 += (timer3b - timer3a)

        # print("prev2 removing previous  ",prev_dict)
        # print("faci1 getting point      ",facing_dict)
        # print("faci2 removing previous  ",facing_dict)

        timer4a = timer()
        for k in prev_dict:
            facing_dict[k] = prev_dict[k]
        timer4b = timer()
        self.t4 += (timer4b - timer4a)

        timer5a = timer()
        facing_dict = {k: facing_dict[k] for k in facing_dict if not isclose(facing_dict[k], 0, abs_tol=3)}
        # print("uni removing returning   ",facing_dict)
        timer5b = timer()
        self.t5 += (timer5b - timer5a)

        if len(facing_dict) == 0:
            return None

        timer6a = timer()
        smallest_angle = min(facing_dict, key=facing_dict.get)
        timer6b = timer()
        self.t6 += (timer6b - timer6a)

        timer7a = timer()
        # print("smallest angle           ",smallest_angle)
        facing_dict = {self.shape.get_point(k) for k in facing_dict if
                       isclose(facing_dict[k], facing_dict[smallest_angle], abs_tol=1)}
        timer7b = timer()
        self.t7 += (timer7b - timer7a)

        # print("keeping smallest         ",facing_dict)

        timer8a = timer()
        if len(facing_dict) > 1:
            facing_dict = {k: k.distance(c) for k in facing_dict}
            smallest_distance = min(facing_dict, key=facing_dict.get)
            # print("closest                  ",smallest_distance)
            timer8b = timer()
            self.t8 += (timer8b - timer8a)
            return smallest_distance
        else:
            timer8b = timer()
            self.t8 += (timer8b - timer8a)
            return get_from_set(facing_dict)
        # need point    remove duplicate
        # need point    remove segment with 0 length
        # need point    remove already used points (including prev and current)
        # need index (need angle)    remove segment returning through previous, that's the segment with angle 0
        # need index (need angle)    get the segment with smallest angle to previous

        return None

    '''
    def filter_segment_clockwise(self, p, c, new_spline):

        timer1a = timer()
        segments = self.shape.get_facing_connected_segment(c)
        prev_segments = self.shape.get_prev_connected_segment(c, True)
        timer1b = timer()
        self.t1 += (timer1b - timer1a)

        p_angle = get_angle_of_vector(p - c, self.__xaxis)
        # print("p_angle",p_angle)

        timer2a = timer()
        prev_dict = {self.shape.get_point(segment_index[0]): segment_index for segment_index in prev_segments}
        facing_dict = {self.shape.get_point(segment_index[1]): segment_index for segment_index in segments}
        timer2b = timer()
        self.t2 += (timer2b - timer2a)

        # print("prev1 getting point      ",prev_dict)

        timer3a = timer()
        prev_dict = {prev_dict[k][0]: self.m1(p_angle, prev_dict[k][0]) for k in prev_dict if k not in new_spline}
        facing_dict = {facing_dict[k][1]: self.m2(p_angle, facing_dict[k][0]) for k in facing_dict if
                       k not in new_spline}

        timer3b = timer()
        self.t3 += (timer3b - timer3a)

        # print("prev2 removing previous  ",prev_dict)
        # print("faci1 getting point      ",facing_dict)
        # print("faci2 removing previous  ",facing_dict)

        timer4a = timer()
        for k in prev_dict:
            facing_dict[k] = prev_dict[k]
        timer4b = timer()
        self.t4 += (timer4b - timer4a)

        timer5a = timer()
        facing_dict = {k: facing_dict[k] for k in facing_dict if not isclose(facing_dict[k], 0, abs_tol=3)}
        # print("uni removing returning   ",facing_dict)
        timer5b = timer()
        self.t5 += (timer5b - timer5a)

        if len(facing_dict) == 0:
            return None

        timer6a = timer()
        smallest_angle = min(facing_dict, key=facing_dict.get)
        timer6b = timer()
        self.t6 += (timer6b - timer6a)

        timer7a = timer()
        # print("smallest angle           ",smallest_angle)
        facing_dict = {self.shape.get_point(k) for k in facing_dict if
                       isclose(facing_dict[k], facing_dict[smallest_angle], abs_tol=1)}
        timer7b = timer()
        self.t7 += (timer7b - timer7a)

        # print("keeping smallest         ",facing_dict)

        timer8a = timer()
        if len(facing_dict) > 1:
            facing_dict = {k: k.distance(c) for k in facing_dict}
            smallest_distance = min(facing_dict, key=facing_dict.get)
            # print("closest                  ",smallest_distance)
            timer8b = timer()
            self.t8 += (timer8b - timer8a)
            return smallest_distance
        else:
            timer8b = timer()
            self.t8 += (timer8b - timer8a)
            return get_from_set(facing_dict)
        # need point    remove duplicate
        # need point    remove segment with 0 length
        # need point    remove already used points (including prev and current)
        # need index (need angle)    remove segment returning through previous, that's the segment with angle 0
        # need index (need angle)    get the segment with smallest angle to previous

        return None
    '''

    def get_output(self):
        output = deque()
        for spline_class in self.shape_output:
            output.append(spline_class.spline_list)
        return output

    def m1(self, p_angle, x):
        a = self.shape.get_angle_for_index(x) - 180 - p_angle
        while a < 0:
            a += 360
        while a >= 360:
            a -= 360
        return a

    def m2(self, p_angle, x):
        a = self.shape.get_angle_for_index(x) - p_angle
        while a < 0:
            a += 360
        while a >= 360:
            a -= 360
        return a

    def already_use(self, segment):
        used = self.s1x
        if segment[0].xe in used:
            if segment[0].ye in used[segment[0].xe]:
                if segment[1].xe in used[segment[0].xe][segment[0].ye]:
                    if segment[1].ye in used[segment[0].xe][segment[0].ye][segment[1].xe]:
                        return True
        return False

    def add_to_used(self, segment):
        self.s1x[segment[0].xe][segment[0].ye][segment[1].xe][segment[1].ye].add(segment)

    def is_used_point(self,point):
        if point.xe in self.s3x:
            if point.ye in self.s3x[point.xe]:
                        return True
