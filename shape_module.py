import functools
from collections import defaultdict
from itertools import permutations, product
from math import fabs
from operator import itemgetter

from general_cache_module import AngleCache
from my_utility_module import get_from_set
from point_module import Point
from vector_module import get_angle_of_vector


class Shapes:
    def __init__(self):
        self.__points = []
        self.__isClosed = []
        self.__pa = functools.partial(defaultdict, set)
        self.index = defaultdict(self.__pa)
        self.point_approximation = Point.e
        self.__angle_index = []
        self.__angle_dict = defaultdict(set)
        self.__xaxis = Point((1, 0, 0))
        self.angle_precision = 10
        self.get_seg = None
        self.pre_seg = None
        self.segment_array = []

    def rebuild_all_index(self):
        self.rebuild_points()
        self.build_index("first")
        self.build_angle()
        self.set_full_spline_segment_array(True)

    def colinear_angle(self, angle1, angle2):
        if fabs(angle2 - angle1) < self.angle_precision:
            return True
        else:
            angle2 = (angle2 % 360) % 180
            if angle2 > 180-self.angle_precision:
                angle2 -= 180
            angle1 = (angle1 % 360) % 180
            if angle1 > 180-self.angle_precision:
                angle1 -= 180
            return fabs(angle2 - angle1) < self.angle_precision

    def same_angle(self, angle1, angle2):

        return fabs(angle2 - angle1) < self.angle_precision

    '''
    def same_angle_at(self, angle1, angle2, prop):
        return angle2 - prop < angle1 < angle2 + prop

    def get_by_angle(self, angle):
        appro = angle / self.angle_precision
        point_set = self.__angle_dict[appro].union(self.__angle_dict[appro + 1]).union(self.__angle_dict[appro - 1])

    def get_by_same_angle(self, point_index):
        return self.get_by_angle(self.get_angle_for_index(point_index))
    
    def get_by_appro_angle(self, appro):
        point_set = self.__angle_dict[appro].union(self.__angle_dict[appro + 1]).union(self.__angle_dict[appro - 1])

    def build_angle(self):
        self.__angle_dict.clear()
        self.__angle_index = []
        for ishape, oshape in enumerate(self.__points):
            self.__angle_index.append([])
            for ispline, ospline in enumerate(oshape):
                self.__angle_index[-1].append([])
                for iknot, oknot in enumerate(ospline):
                    p1_index = (ishape, ispline, iknot)
                    angle = get_angle_of_vector(self.get_point(self.next_point(p1_index, True)) - oknot,
                                                     self.__xaxis)
                    self.__angle_index[p1_index[0]][p1_index[1]].append(angle)
                    self.__angle_dict[angle].add(p1_index)

    '''

    def build_angle(self):
        self.__angle_index = []
        for ishape in range(len(self.points)):
            self.__angle_index.append([])
            for ispline in range(len(self.points[ishape])):
                self.__angle_index[-1].append([])
                l = len(self.points[ishape][ispline])
                self.__angle_index[-1][-1].extend(
                    [AngleCache((ishape, ispline, iknot), (ishape, ispline, iknot + 1)) for iknot in range(l - 1)])
                if self.is_closed((ishape, ispline)):
                    self.__angle_index[-1][-1].append(AngleCache((ishape, ispline, l - 1), (ishape, ispline, 0)))

    def get_angle_for_segment(self, segment):
        if segment[1][2] == 0:
            return self.__angle_index[segment[0][0]][segment[0][1]][segment[0][2]].get_angle()
        origin = min(segment, key=itemgetter(2))
        angle = self.__angle_index[segment[0][0]][segment[0][1]][origin[2]].get_angle()
        if origin == segment[1]:
            return abs(180 - angle)

    def get_angle_for_index(self, index):
        # #print("angle ",index)
        return self.__angle_index[index[0]][index[1]][index[2]].get_angle()

    def get_closest_angle(self, index):
        a = (self.get_angle_for_index(index) % 360) % 180
        if a > 360 - self.angle_precision:
            a -= 360
        return a

    def get_closest_reverse_angle(self, index):
        a = ((self.get_angle_for_index(index) - 180) % 360) % 180
        if a > 360 - self.angle_precision:
            a -= 360
        return a

    def set_angle_for_index(self, angle, index):
        self.__angle_index[index[0]][index[1]][index[2]] = angle
        self.__angle_dict[angle].add(index)

    def add_to_index(self, point_index):
        point = self.get_point(point_index)
        self.index[point.xe][point.ye].add(point_index)

    def remove_from_index(self, point_index):
        point = self.get_point(point_index)
        self.index[point.xe][point.ye].remove(point_index)

    def get_from_index(self, point_instance):
        return {x for x in self.samples_from_index(point_instance) if self.get_point(x) == point_instance}

    def get_from_index_by_e(self, xe, ye):
        p = get_from_set(self.index[xe][ye])
        return self.samples_from_index(p)

    def samples_from_index(self, point_instance):
        x_y_keys = set()
        for x_key in set(self.index.keys()).intersection(range(point_instance.xe - 1, point_instance.xe + 2)):
            for y_key in set(self.index[x_key].keys()).intersection(
                    range(point_instance.ye - 1, point_instance.ye + 2)):
                x_y_keys.add((x_key, y_key))
        point_set = set()
        for x, y in x_y_keys:
            point_set.update(self.index[x][y])
        return point_set

    def points_at_distance(self, point_instance, distance):
        distance = int(distance / Point.e) + 2
        x_y_keys = set()
        for x_key in set(self.index.keys()).intersection(
                range(point_instance.xe - distance, point_instance.xe + distance)):
            for y_key in set(self.index[x_key].keys()).intersection(
                    range(point_instance.ye - distance, point_instance.ye + distance)):
                x_y_keys.add((x_key, y_key))
        point_set = set()
        for x, y in x_y_keys:
            point_set.update(self.index[x][y])
        return point_set

    def rebuild_points(self):
        new_points = []
        new_closed_ar = []
        for ishape, oshape in enumerate(self.points):
            if len(oshape) > 0:
                new_shape = []
                new_closed = []
                for ispline, ospline in enumerate(oshape):
                    if len(ospline) > 1:
                        new_spline = [oknot for oknot in ospline]
                        new_shape.append(new_spline)
                        new_closed.append(self.isClosed[ishape][ispline])

                if len(new_shape) > 0:
                    new_points.append(new_shape)
                    new_closed_ar.append(new_closed)
        self.points = new_points
        self.isClosed = new_closed_ar

    def reassign_e(self,e):
        Point.e = e
        for oshape in self.points:
            for ospline in oshape:
                for oknot in ospline:
                    oknot.x = oknot.x
                    oknot.y = oknot.y

    def build_index(self, name):
        self.index.clear()
        self.__pa = functools.partial(defaultdict, set)
        self.index = defaultdict(self.__pa)
        for ishape in range(len(self.points)):
            for ispline in range(len(self.points[ishape])):
                for iknot in range(len(self.points[ishape][ispline])):
                    self.add_to_index((ishape, ispline, iknot))
        '''
        for x in self.index.keys():
            for y in self.index[x]:
                #print(name,x,y,self.index[x][y])
        '''
        # #print("##printing dict------------")
        # for xdict in self.index.values():
        # for ydict in xdict.values():
        # #print(ydict)
        # #print("##printing dict------------")

    def add_points_data(self, data, isClosed):
        for oshape in data:
            new_shape = []
            for ospline in oshape:
                # #print("data is " + str(ospline))
                new_spline = [Point(x) for x in ospline]
                new_shape.append(new_spline)
            self.points.append(new_shape)
        for oshape in isClosed:
            is_close_shape = []
            for ospline in oshape:
                # #print("data is " + str(ospline))
                new_spline = ospline
                is_close_shape.append(new_spline)
            self.isClosed.append(is_close_shape)

    @property
    def points(self):
        return self.__points

    @points.setter
    def points(self, points):
        self.__points = points

    @property
    def isClosed(self):
        return self.__isClosed

    @isClosed.setter
    def isClosed(self, isClosed):
        self.__isClosed = isClosed

    def get_indexes(self, point):
        return self.get_from_index(point)

    def get_point(self, index):
        return self.points[index[0]][index[1]][index[2]]

    def is_closed(self, index):
        return self.isClosed[index[0]][index[1]]

    def next_point(self, index, cycling):
        last_knot = len(self.points[index[0]][index[1]]) - 1

        if 0 > index[2] > last_knot:
            return None

        if index[2] == last_knot:
            if cycling:
                next_point = (index[0], index[1], 0)
            else:
                return None
        else:
            next_point = (index[0], index[1], index[2] + 1)
        return next_point

    def prev_point(self, index, cycling):
        last_knot = len(self.points[index[0]][index[1]]) - 1

        if index[2] < 0 or index[2] > last_knot:
            return None

        if index[2] == 0:
            if cycling:
                prev = (index[0], index[1], last_knot)
            else:
                return None
        else:
            prev = (index[0], index[1], index[2] - 1)

        return prev

    def get_segment(self, index):
        last_knot = len(self.points[index[0]][index[1]]) - 1

        if index[2] < 0 or index[2] > last_knot:
            return None

        next_start = (index[0], index[1], index[2])
        if next_start[2] == last_knot:
            if self.isClosed[index[0]][index[1]]:
                next_end = (index[0], index[1], 0)
            else:
                return None
        else:
            next_end = (index[0], index[1], index[2] + 1)

        s = (next_start, next_end)
        return s

    def next_segment(self, index, cycling):
        last_knot = len(self.points[index[0]][index[1]])

        if 0 > index[2] > last_knot:
            return None

        if index[2] == last_knot:
            if cycling and self.isClosed[index[0]][index[1]]:
                next_start = (index[0], index[1], 0)
                next_end = (index[0], index[1], 1)
            else:
                return None

        else:
            next_start = (index[0], index[1], index[2] + 1)
            next_end = (index[0], index[1], index[2] + 2)

        s = (next_start, next_end)
        return s

    def prev_segment(self, index, cycling):
        last_knot = len(self.points[index[0]][index[1]])

        if 0 > index[2] > last_knot:
            return None

        if index[2] == 0:
            if cycling:
                if self.isClosed[index[0]][index[1]]:
                    prev_start = (index[0], index[1], last_knot - 1)
                    prev_end = (index[0], index[1], 0)
                else:
                    return None
            else:
                return None
        else:
            prev_start = (index[0], index[1], index[2] - 1)
            prev_end = (index[0], index[1], index[2])

        s = (prev_start, prev_end)
        return s

    def get_all_connected_segment(self, point_instance, cycling):
        index_set = self.get_from_index(point_instance)
        return {self.get_segment(index) for index in index_set}.union(
            {self.prev_segment(index, cycling) for index in index_set}).difference({None})

    def get_facing_connected_segment(self, point):
        index_set = self.get_from_index(point)
        return {self.get_segment(index) for index in index_set}.difference({None})

    def get_prev_connected_segment(self, point, cycling):
        index_set = self.get_from_index(point)
        return {self.prev_segment(index, cycling) for index in index_set}.difference({None})

    def get_facing_connected_point(self, point):
        index_set = self.get_from_index(point)
        return {x[1] for x in ({self.get_segment(index) for index in index_set}.difference({None}))}

    def get_connected_points(self, point, cycling):
        index_set = self.get_from_index(point)
        '''
        #print("index set",index_set)
        for index in index_set:
            segment = self.get_segment(index)
            
            seg_pos = [self.get_point(x) for x in segment]
            preview = self.prev_segment(index,cycling)
            prev_pos = [self.get_point(x) for x in preview]
            #print("x[1]",segment)
            #print("x[1]",seg_pos)
            #print("x[0", preview)
            #print("x[0", prev_pos)
        '''

        return {x[1] for x in {self.get_segment(index) for index in index_set} if
                x is not None}.union(
            {x[0] for x in {self.prev_segment(index, cycling) for index in index_set} if x is not None})

    def get_connected_points_instances(self, point_instance, cycling):
        point_index_set = self.get_from_index(point_instance)
        return {self.get_point(x[1]) for x in {self.get_segment(index) for index in point_index_set} if
                x is not None}.union(
            {self.get_point(point_index[0]) for point_index in
             {self.prev_segment(index, cycling) for index in point_index_set} if point_index is not None})

    def move_cluster(self, p, new_coordinate):

        point_set = self.get_from_index(p)
        # #print("move",p,"point set",point_set,new_coordinate)
        for point_index in point_set:
            self.get_point(point_index).set_position(new_coordinate)

    def print_points(self):
        print("shape----")
        for oshape in self.points:
            for ospline in oshape:
                print(str(ospline))
        print("----shape")

    def segment_array_to_string(self, arr):
        if len(arr) == 0:
            return "empty"
        s1 = None
        for s2 in arr:
            s1 = s2
            break
        if len(s1) == 2:
            return [(self.get_point(seg[0]), self.get_point(seg[1])) for seg in arr]
        else:
            return [(self.get_point(seg[0]), self.get_point(seg[1]), seg[2]) for seg in arr]

    def remove_knot(self, knot_index):
        knot_companion_index = None
        if not self.isClosed[knot_index[0]][knot_index[1]]:
            last = len(self.points[knot_index[0]][knot_index[1]]) - 1
            if knot_index[2] == 0:
                knot_companion_index = (knot_index[0], knot_index[1], last)
            if knot_index[2] == last:
                knot_companion_index = (knot_index[0], knot_index[1], 0)

            if knot_companion_index is not None:
                p1 = self.get_point(knot_index)
                p2 = self.get_point(knot_companion_index)
                if p1 == p2:
                    self.isClosed[knot_index[0]][knot_index[1]] = True

        del self.points[knot_index[0]][knot_index[1]][knot_index[2]]

    def add_computed_spline(self, spline_array):
        self.points.append([spline_array])
        ishape = len(self.points)-1
        ispline = 0
        self.segment_array.append([])
        self.__angle_index.append([])
        self.__angle_index[-1].append([])
        l = len(spline_array)
        self.__angle_index[-1][-1].extend(
                    [AngleCache((ishape, ispline, iknot), (ishape, ispline, iknot + 1)) for iknot in range(l - 1)])
        for iknot in range(l-1):
            self.add_to_index((ishape,ispline,iknot))
            s = ((ishape, ispline, iknot), (ishape, ispline, iknot + 1))
            self.segment_array[-1].append(s)
            point_g = self.points[ishape][ispline][iknot]
            point_p = self.points[ishape][ispline][iknot + 1]
            self.get_seg[point_g.xe][point_g.ye].add(s)
            self.pre_seg[point_p.xe][point_p.ye].add(s)
        self.isClosed.append([False])


    def add_point_between(self,new_point, a1, a2):
        #print("starting insert point",new_point,"between",a1,"and",a2)
        point_a1_segment_set = self.get_seg_from_index(a1).union(self.pre_seg_from_index(a1))
        for segment in point_a1_segment_set:
            s_points = (self.get_point(segment[0]),self.get_point(segment[1]))
            if {a1,a2} == set(s_points):
                ishape = segment[0][0]
                ispline =segment[0][1]
                ospline = self.points[ishape][ispline]
                #print("before",ospline)
                a_position = segment[1][2]
                self.remove_from_get_from_index(((ishape,ispline,a_position-1),(ishape,ispline,a_position)))
                self.remove_from_pre_from_index(((ishape,ispline,a_position-1),(ishape,ispline,a_position)))
                for iknot in range(a_position,len(ospline)-1):
                    s = ((ishape,ispline,iknot),(ishape,ispline,iknot+1))
                    self.remove_from_index((ishape,ispline,iknot))
                    self.remove_from_get_from_index(s)
                    self.remove_from_pre_from_index(s)
                self.remove_from_index((ishape,ispline,len(ospline)-1))
                if self.isClosed[ishape][ispline]:
                    self.remove_from_get_from_index(((ishape,ispline,len(ospline)-1),(ishape,ispline,0)))
                    self.remove_from_pre_from_index(((ishape,ispline,len(ospline)-1),(ishape,ispline,0)))

                self.points[ishape][ispline].insert(a_position,new_point)
                self.add_to_get_from_index(((ishape,ispline,a_position-1),(ishape,ispline,a_position)))
                self.add_to_pre_from_index(((ishape,ispline,a_position-1),(ishape,ispline,a_position)))
                for iknot in range(a_position,len(ospline)-1):
                    s = ((ishape,ispline,iknot),(ishape,ispline,iknot+1))
                    self.add_to_index((ishape,ispline,iknot))
                    self.add_to_get_from_index(s)
                    self.add_to_pre_from_index(s)
                self.add_to_index((ishape,ispline,len(ospline)-1))
                if self.isClosed[ishape][ispline]:
                    self.add_to_get_from_index(((ishape,ispline,len(ospline)-1),(ishape,ispline,0)))
                    self.add_to_pre_from_index(((ishape,ispline,len(ospline)-1),(ishape,ispline,0)))
                self.__angle_index[ishape][ispline] = [AngleCache((ishape, ispline, iknot), (ishape, ispline, iknot + 1)) for iknot in range(len(ospline)-1)]
                if self.is_closed((ishape, ispline)):
                    self.__angle_index[ishape][ispline].append(AngleCache((ishape, ispline, len(ospline) - 1), (ishape, ispline, 0)))
                #print("after",ospline)

    def get_spline_segment_array(self):
        spline_array = []
        for ishape in range(len(self.points)):
            for ispline in range(len(self.points[ishape])):
                l = len(self.points[ishape][ispline])
                spline_array.append(
                    [((ishape, ispline, iknot), (ishape, ispline, iknot + 1)) for iknot in
                     range(len(self.points[ishape][ispline]) - 1)])
                if self.is_closed((ishape, ispline)):
                    spline_array[-1].append(((ishape, ispline, l - 1), (ishape, ispline, 0)))
        return spline_array

    def set_full_spline_segment_array(self, cycling):
        del self.segment_array[:]
        get_py = functools.partial(defaultdict, set)
        self.get_seg = defaultdict(get_py)
        pre_py = functools.partial(defaultdict, set)
        self.pre_seg = defaultdict(pre_py)
        for ishape in range(len(self.points)):
            for ispline in range(len(self.points[ishape])):
                self.segment_array.append([])
                l = len(self.points[ishape][ispline])
                for iknot in range(l - 1):
                    s = ((ishape, ispline, iknot), (ishape, ispline, iknot + 1))
                    self.segment_array[-1].append(s)
                    point_g = self.points[ishape][ispline][iknot]
                    point_p = self.points[ishape][ispline][iknot + 1]
                    self.get_seg[point_g.xe][point_g.ye].add(s)
                    self.pre_seg[point_p.xe][point_p.ye].add(s)

                if self.is_closed((ishape, ispline)):
                    s = ((ishape, ispline, l - 1), (ishape, ispline, 0))
                    self.segment_array[-1].append(s)
                    point_g = self.points[ishape][ispline][l - 1]
                    self.get_seg[point_g.xe][point_g.ye].add(s)
                    if cycling:
                        point_p = self.points[ishape][ispline][0]
                        self.pre_seg[point_p.xe][point_p.ye].add(s)

    def get_seg_from_index(self, point_instance):
        seg = set()
        for x_key in range(point_instance.xe - 1, point_instance.xe + 2):
            if x_key in self.get_seg:
                for y_key in range(point_instance.ye - 1, point_instance.ye + 2):
                    if y_key in self.get_seg[x_key]:
                        seg.update(self.get_seg[x_key][y_key])
        return seg

    def remove_from_get_from_index(self,segment):
        removed = False
        p = self.get_point(segment[0])
        if p.xe in self.get_seg.keys():
            if p.ye in self.get_seg[p.xe].keys():
                if segment in self.get_seg[p.xe][p.ye]:
                    removed =True
                    #print("yyyeeewwwwwwwwwwww get removed",segment)
                    self.get_seg[p.xe][p.ye].remove(segment)

    def add_to_get_from_index(self,segment):
        p = self.get_point(segment[0])
        self.get_seg[p.xe][p.ye].add(segment)

    def remove_from_pre_from_index(self,segment):
        removed = False
        p = self.get_point(segment[1])
        if p.xe in self.pre_seg.keys():
            if p.ye in self.pre_seg[p.xe].keys():
                if segment in self.pre_seg[p.xe][p.ye]:
                    #print  ("yyyyyyyyy pre yes removed yyyyyyyyyyy")
                    removed = True
                    self.pre_seg[p.xe][p.ye].remove(segment)


    def add_to_pre_from_index(self,segment):
        p = self.get_point(segment[1])
        self.pre_seg[p.xe][p.ye].add(segment)
    
    def get_seg_from_index_by_e(self, xe,ye):
        seg = set()
        for x_key in range(xe - 1, xe + 2):
            if x_key in self.get_seg:
                for y_key in range(ye - 1, ye + 2):
                    if y_key in self.get_seg[x_key]:
                        seg.update(self.get_seg[x_key][y_key])
        return seg

    def pre_seg_from_index(self, point_instance):
        seg = set()
        for x_key in range(point_instance.xe - 1, point_instance.xe + 2):
            if x_key in self.pre_seg:
                for y_key in range(point_instance.ye - 1, point_instance.ye + 2):
                    if y_key in self.pre_seg[x_key]:
                        seg.update(self.pre_seg[x_key][y_key])
        return seg
    
    def pre_seg_from_index_by_e(self, xe,ye):
        seg = set()
        for x_key in range(xe - 1, xe + 2):
            if x_key in self.pre_seg:
                for y_key in range(ye - 1, ye + 2):
                    if y_key in self.pre_seg[x_key]:
                        seg.update(self.pre_seg[x_key][y_key])
        return seg

    def get_connected_point_instance_from_index(self, point_instance):
        return {self.get_point(x[1]) for x in self.get_seg_from_index(point_instance)}.union(
            {self.get_point(x[0]) for x in self.pre_seg_from_index(point_instance)})

    def connected_point_instance_angle_from_index(self, point_instance):
        return {(self.get_point(x[1]), self.get_angle_for_index(x[0])) for x in
                self.get_seg_from_index(point_instance)}.union(
            {(self.get_point(x[0]), self.get_angle_for_index(x[0])) for x in self.pre_seg_from_index(point_instance)})

    def connected_point_instance_closest_angle_from_index(self, point_instance):
        return {(self.get_point(x[1]), self.get_closest_angle(x[0])) for x in
                self.get_seg_from_index(point_instance)}.union(
            {(self.get_point(x[0]), self.get_closest_reverse_angle(x[0])) for x in
             self.pre_seg_from_index(point_instance)})

    def connected_segment_index_closest_angle_from_index(self, point_instance):
        return {(x[0], x[1], self.get_closest_angle(x[0])) for x in self.get_seg_from_index(point_instance)}.union(
            {(x[1], x[0], self.get_closest_reverse_angle(x[0])) for x in self.pre_seg_from_index(point_instance)})

    def connected_segment_index_angle_from_index(self, point_instance):
        return {(x[0], x[1], self.get_angle_for_index(x[0])) for x in
                self.get_seg_from_index(point_instance)}.union(
            {(x[1], x[0], self.get_angle_for_index(x[0])) for x in self.pre_seg_from_index(point_instance)})

    def connected_segment_index_closest_angle_from_index_by_e(self, xe,ye):
        return {(x[0], x[1], self.get_closest_angle(x[0])) for x in self.get_seg_from_index_by_e(xe,ye)}.union(
            {(x[1], x[0], self.get_closest_reverse_angle(x[0])) for x in self.pre_seg_from_index_by_e(xe,ye)})

    def connected_segment_index_angle_from_index_by_e(self, xe,ye):
        return {(x[0], x[1], self.get_angle_for_index(x[0])) for x in self.get_seg_from_index_by_e(xe,ye)}.union(
            {(x[1], x[0], self.get_angle_for_index(x[0])-180) for x in self.pre_seg_from_index_by_e(xe,ye)})

    def remove_consecutive_duplicate_point(self):
        point_to_remove = set()
        for ishape, oshape in enumerate(self.points):
            for ispline, ospline in enumerate(oshape):
                for iknot, p1 in enumerate(ospline):
                    p1_index = (ishape, ispline, iknot)
                    p2_index = self.next_point(p1_index, True)

                    p2 = self.get_point(p2_index)
                    if p1 == p2:
                        point_to_remove.add(p1_index)

        point_to_remove = sorted(point_to_remove, reverse=True)
        for point in point_to_remove:
            self.remove_knot(point)
