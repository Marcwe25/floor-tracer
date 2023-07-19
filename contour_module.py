from collections import defaultdict
from math import fabs
from operator import itemgetter

from intersection_module import get_extended_intersection
from my_utility_module import get_from_set, isclose
from point_module import Point
from vector_module import get_angle, get_angle_of_vector, closest_point_on_line_param
from pprint import pprint

class ContourTracer:

    def __init__(self, shape):
        self.max_bridge_size = 300
        self.shape = shape
        self.previous = None
        self.current = None
        self.max = 20
        self.first = None
        self.counter = 2
        self.contour = []
        self.use_bridge = True
        self.max_wall_width = 40
        self.xaxis = Point((1, 0, 0))
        self.angle_precision = 10

    def draw_contour(self):
        for ishape in range(len(self.shape.points)):
            for ispline in range(len(self.shape.points[ishape])):
                self.max += len(self.shape.points[ishape][ispline])

        self.get_starting_points()
        while self.current is not None and self.current != self.first and self.counter < self.max:
            self.counter += 1
            next_point = self.next_point_on_contour(self.previous, self.current)
            if next_point is not None:
                if self.use_bridge and get_angle(self.current, self.previous, next_point) < 180 - self.angle_precision:
                    # #print("checking bridge option", self.previous, self.current, next_point, get_angle(self.current, self.previous, next_point))
                    bridge = self.find_bridge(self.previous, self.current)
                    # #print("bridge for previous",self.previous,"current",self.current,bridge)
                    if isinstance(bridge[0], Point) and self.current.distance(bridge[0]) < self.max_bridge_size:
                        points_to_filter = {next_point, bridge[0]}
                        point_to_go = self.filter_point_to_go(self.previous, self.current, points_to_filter)
                        if point_to_go == bridge[0]:
                            self.shape.add_computed_spline([self.current, bridge[0]])
                            self.add_bridge_to_shape(bridge)
                            self.find_bridge_wall(self.previous, self.current, bridge)
                            self.add_to_contour(bridge[1], bridge[0])
                        else:
                            self.add_to_contour(next_point)
                    else:
                        self.add_to_contour(next_point)
                else:
                    self.add_to_contour(next_point)
            else:
                self.add_to_contour(None)
        return self.contour

    def add_to_contour(self, next_current, next_previous=None):
        if next_previous is None:
            self.previous = self.current
        else:
            self.previous = next_previous
            self.contour.append(next_previous)
        self.current = next_current
        if next_current is not None:
            self.contour.append(next_current)

    def get_starting_points(self):
        shape = self.shape
        min_x_index = min(self.shape.index)
        min_y_index = min(self.shape.index[min_x_index])
        self.previous = shape.get_point(get_from_set(shape.index[min_x_index][min_y_index]))
        self.first = Point(self.previous.get_position())
        previous = self.previous
        if len(shape.index[min_x_index]) == 1:
            points = {shape.get_point(index) for index in shape.get_connected_points(previous, True)}
            points_angles = {(point, get_angle(previous, previous + Point((0, -1, 0)), point)) for point in points}
            points_angles = {item for item in points_angles if item[1] <= 180 or isclose(item[1], 180, abs_tol=0.1)}
            max_angle = max(points_angles, key=itemgetter(1))
            points_with_max_angle = {item for item in points_angles if isclose(item[1], max_angle[1], abs_tol=1e-01)}
            point_min_in_y = min({point for point in points_with_max_angle}, key=lambda item: item[0].y)
            self.current = point_min_in_y[0]
        else:
            y_sorted = sorted(shape.index[min_x_index].keys())
            self.current = shape.get_point(get_from_set(shape.index[min_x_index][y_sorted[1]]))

        self.contour = [self.previous, self.current]

    def next_point_on_contour(self, a1, a2):
        connected_points = self.shape.get_connected_points(a2, True)
        connected_points = {self.shape.get_point(x) for x in connected_points}
        # #print("con",a2,connected_points)
        if len(connected_points) == 1 and get_from_set(connected_points) == a1:
            bridge = self.find_bridge(a1, a2)
            if bridge is not None and bridge[0] != 0:
                connected_points.add(bridge)
                result = self.filter_point_to_go(a1, a2, connected_points)
                if result == bridge[0]:
                    self.shape.add_computed_spline([self.current, bridge[0]])
                    self.add_bridge_to_shape(bridge)
                    self.find_bridge_wall(self.previous, self.current, bridge)
                    return result

        return self.filter_point_to_go(a1, a2, connected_points)

    def add_bridge_to_shape(self,bridge):
        #print("adding bridge to shape")
        b_exist = False
        if bridge[0].xe in self.shape.index:
            if bridge[0].ye in self.shape.index[bridge[0].xe]:
                b_exist = True
        if not b_exist:
            for conn_point in bridge[2]:
                #print("adding from bridge to shape",[bridge[0],conn_point])
                self.shape.add_computed_spline([bridge[0],conn_point])

    def find_bridge(self, a1, a2):
        # #print("looking for bridge")
        bridge_items = get_extended_intersection(self.shape, a1, a2, 3)
        points = bridge_items.keys()
        points = sorted(points, key=lambda x: x.distance(a2))
        #print("bridge points",points)
        for point in points:
            bridge_end = self.bridge_continuity(a1, a2, (point, bridge_items[point]))
            if bridge_end:
                r = (point, bridge_end,tuple(bridge_items[point]))
                return r
        r = (0, [])
        #print("no bridge end")
        return r

    def bridge_continuity(self, a1, a2, bridge_item):
        bridge_middle = bridge_item[0]
        potential_points = bridge_item[1]
        bridge_end = self.filter_point_to_go(a2, bridge_middle, potential_points)
        return bridge_end

    def filter_point_to_go(self, a1, a2, connected_points):

        if not isinstance(connected_points, set):
            connected_points = set(connected_points)

        if len(connected_points) == 0:
            return None

        input_list = list(connected_points)
        # #print("curr",a2,"prev",a1)
        # #print("c input list", input_list)
        filtered = [(i, x) if isinstance(x, Point) else (i, x[0]) for i, x in enumerate(input_list)]
        # #print("c point", filtered)

        # filtered = [(i, x) for i, x in filtered if x not in self.contour and x != a2 and x != a1]
        filtered = [(i, x) for i, x in filtered if x != a2 and x != a1]
        # #print("c remove prev and curr", filtered)

        filtered = [[i, x, get_angle(a2, a1, x)] for i, x in filtered]
        # #print("c with angle", filtered)
        for item in filtered:
            if item[2]>=360-self.angle_precision:
                item[2] = item[2]-360
        filtered = [[i,x,angle] for i,x,angle in filtered if angle > self.angle_precision]
        if len(filtered) == 0:
            return None
        if len(filtered) == 1:
            return filtered[0][1]
        biggest_angle = max(filtered, key=itemgetter(2))
        # #print("c big angle", biggest_angle)
        filtered = [(i, x, x.distance(a2)) for i, x, an in filtered if isclose(biggest_angle[2], an, abs_tol=3)]
        # #print("c those big angle", filtered)

        closest_point = min(filtered, key=itemgetter(2))
        # #print("c closest", closest_point)

        i = closest_point[0]
        return input_list[i]

    def find_bridge_wall(self, previous, current, bridge):
        #print("------------------")
        #print("==================")
        #print("current, starting bridge wall, previous", previous, "current", current, "bridge",bridge)
        p_angle = ((get_angle_of_vector(current - previous, self.xaxis)) % 360) % 180
        #print("current, p_angle", p_angle)
        conn_seg = self.shape.get_seg_from_index(current)
        #print("current, get self.shape.get_seg_from_index(current)", self.shape.segment_array_to_string(conn_seg))
        conn_seg = {(seg[0], seg[1], self.shape.get_closest_angle(seg[0])) for seg in conn_seg}
        #print("current, get with angle", self.shape.segment_array_to_string(conn_seg))
        conn_seg = [seg for seg in conn_seg if not self.shape.same_angle(p_angle, seg[2])]
        #print("current, get filter by angle", self.shape.segment_array_to_string(conn_seg))

        prev_segm = self.shape.pre_seg_from_index(current)
        #print("current, pre self.shape.pre_seg_from_index(current)", self.shape.segment_array_to_string(prev_segm))
        prev_segm = {(seg[0], seg[1], self.shape.get_closest_reverse_angle(seg[0])) for seg in prev_segm}
        #print("current, pre current, with angle", self.shape.segment_array_to_string(prev_segm))
        prev_segm = [seg for seg in prev_segm if not self.shape.same_angle(p_angle, seg[2])]
        #print("current, pre filter by angle", self.shape.segment_array_to_string(prev_segm))

        bridge_angle = ((get_angle_of_vector(bridge[1] - bridge[0], self.xaxis)) % 360) % 180
        #print("bridge, bridge_angle", bridge_angle)
        bridge_seg = (self.shape.get_seg_from_index(bridge[0]))
        #print("bridge, get self.shape.get_seg_from_index(bridge[0])", self.shape.segment_array_to_string(bridge_seg))
        bridge_seg = {(seg[0], seg[1], self.shape.get_closest_angle(seg[0])) for seg in bridge_seg}
        #print("bridge, get with angle", self.shape.segment_array_to_string(bridge_seg))
        bridge_seg = [seg for seg in bridge_seg if not self.shape.same_angle(bridge_angle, seg[2])]
        #print("bridge, get filter by angle", self.shape.segment_array_to_string(bridge_seg))

        bridge_prev_segm = self.shape.pre_seg_from_index(bridge[0])
        #print("bridge, pre self.shape.pre_seg_from_index(bridge[0])", self.shape.segment_array_to_string(bridge_prev_segm))
        bridge_prev_segm = {(seg[0], seg[1], self.shape.get_closest_reverse_angle(seg[0])) for seg in bridge_prev_segm}
        #print("bridge, pre with angle", self.shape.segment_array_to_string(bridge_prev_segm))
        bridge_prev_segm = [seg for seg in bridge_prev_segm if not self.shape.same_angle(bridge_angle, seg[2])]
        #print("bridge, pre filter by angle", self.shape.segment_array_to_string(bridge_prev_segm))

        current_angle_centric = defaultdict(set)
        for seg in conn_seg:
            current_angle_centric[seg[2]].add(self.shape.get_point(seg[1]))
        for seg in prev_segm:
            current_angle_centric[seg[2]].add(self.shape.get_point(seg[0]))

        bridge_angle_centric = defaultdict(set)
        for seg in bridge_seg:
            bridge_angle_centric[seg[2]].add(self.shape.get_point(seg[1]))
        for seg in bridge_prev_segm:
            bridge_angle_centric[seg[2]].add(self.shape.get_point(seg[0]))

        #print("current_angle_centric",current_angle_centric)
        #print("bridge_angle_centric",bridge_angle_centric)

        if len(current_angle_centric.keys()) == 0:
            self.find_connection(self.previous, self.current, current_angle_centric)
        if len(bridge_angle_centric.keys()) == 0:
            self.find_connection(bridge[1], bridge[0], bridge_angle_centric)

        #print("connection + _centric",current_angle_centric)
        #print("connection + _centric",bridge_angle_centric)
        for c_angle in current_angle_centric.keys():
            c_point_set = current_angle_centric[c_angle]
            b_point_set = set()
            for b_angle in bridge_angle_centric.keys():
                ##print("angle",c_angle,b_angle,self.shape.same_angle(c_angle, b_angle))
                if self.shape.same_angle(c_angle, b_angle):
                    b_point_set.update(bridge_angle_centric[b_angle])
            #print("b_point_set",b_point_set)
            #print("c_point_set",c_point_set)


            if len(c_point_set) > 0 and len(b_point_set) > 0:
                c_point_set_filtered = {point for point in c_point_set if current.distance(point) <= Point.e + self.max_wall_width}
                b_point_set_filtered = {point for point in b_point_set if bridge[0].distance(point) <= Point.e + self.max_wall_width}
                #print("b_point_set_filtered A",b_point_set_filtered)
                #print("c_point_set_filtered A",c_point_set_filtered)

                if len(c_point_set_filtered)>0 or len(b_point_set_filtered)>0:
                    c_point = None
                    b_point = None
                    if len(c_point_set_filtered)>0:
                        c_point = max(c_point_set_filtered, key=current.distance)
                    if len(b_point_set_filtered)>0:
                        b_point = max(b_point_set_filtered, key=bridge[0].distance)

                    if c_point is None:
                        c_point = current + b_point - bridge[0]
                        #self.shape.add_computed_spline([current,c_point])
                        c_point_set_post = {point for point in c_point_set if closest_point_on_line_param(current, c_point, point) > 1}
                        if len(c_point_set_post)>0:
                            c_conn = min(c_point_set_post, key=c_point.distance)
                            #self.shape.add_computed_spline([c_point,c_conn])
                            #print("adding point",c_point,"between",current,"and",c_conn)
                            self.shape.add_point_between(c_point, current, c_conn)

                    if b_point is None:
                        b_point = bridge[0] + c_point - current
                        #self.shape.add_computed_spline([bridge[0],b_point])
                        b_point_set_post = {point for point in b_point_set if closest_point_on_line_param(bridge[0], b_point, point) > 1}
                        if len(b_point_set_post)>0:
                            b_conn = min(b_point_set_post, key=b_point.distance)
                            #self.shape.add_computed_spline([b_point,b_conn])
                            #print("adding point",b_point,"between",bridge[0],"and",b_conn)
                            self.shape.add_point_between(b_point, bridge[0], b_conn)

                    if c_point!=None and b_point!=None:
                        # #print("adding bridge width", ([c_point, b_point]))
                        self.shape.add_computed_spline([c_point, b_point])


    '''
    def m1(self, x):
        a = ((self.shape.get_angle_for_index(x) - 180) % 360) % 180

        if a>360-self.angle_precision:
            a -= 360
        return a

    def m2(self, x):
        a = (self.shape.get_angle_for_index(x) % 360) % 180
        if a>360-self.angle_precision:
            a -= 360
        return a
    '''

    def find_connection(self, previous, current, current_angle_centric):
        ##print("searching conn", previous, current, current_angle_centric)
        points = self.shape.points_at_distance(current, self.max_wall_width)
        ##print("points",points)
        points = {self.shape.get_point(x) for x in points}
        points = {point for point in points if point!=current and point!=previous}
        points = {(point, tuple(self.shape.connected_point_instance_angle_from_index(point))) for point in points}
        ##print("points 5 ", points)
        points = [(point, self.angle_dict(connection)) for point, connection in points]
        points = [(point, angle_dict) for point, angle_dict in points if len(angle_dict.keys()) == 1]
        ##print("points 9 ", points)
        if len(points)==1:
            ##print("conn found", points)
            for point in points:
                angle = get_angle_of_vector(point[0]-current,self.xaxis)
                angle = angle%360
                if angle > 360 -self.angle_precision:
                    angle -= 360
                current_angle_centric[angle].add(point[0])
                self.shape.add_computed_spline([current, point[0]])

    def angle_dict(self, point_instance_angle_pair):
        d = defaultdict(set)
        for point, angle in point_instance_angle_pair:
            ##print("on angle", angle)
            if angle >360-self.angle_precision:
                ##print("on angle 2",angle)
                angle -= 360
            ##print("on angle 3",angle)
            d[angle].add(point)
        ##print("sdffsasdsaf",angle)
        return d
