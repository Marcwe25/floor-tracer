from collections import defaultdict
from operator import itemgetter
from pprint import pprint

from my_utility_module import get_from_set
from point_module import Point
from vector_module import get_angle


class InternalBuilder:

    def __init__(self, shape):
        print("initializ...")
        self.shape = shape
        self.shape.remove_consecutive_duplicate_point()
        self.shape.build_index("contour")
        self.shape_output = list()
        self.all_points = defaultdict(set)
        self.all_paths = defaultdict(set)
        self.path_s_second_point = defaultdict(set)
        self.used_path = set()

    def build_interior(self):
        index = self.shape.index
        shape = self.shape
        all_points = self.all_points
        all_paths = self.all_paths
        used_path = self.used_path

        for x_keys in index.keys():
            for y_keys in index[x_keys]:
                point_index = get_from_set(index[x_keys][y_keys])
                point = shape.get_point(point_index)
                connected_points = shape.get_connected_points(point, True)
                connected_points = {shape.get_point(x) for x in connected_points}
                #print("connected",point,connected_points)
                all_points[point].update(connected_points)
        connection_points = (i for i in all_points.keys() if len(self.all_points[i]) > 2)
        #print("lookng in get sub")
        for point in connection_points:
            self.get_sub_paths(point)
        '''
        for path_set in all_paths.values():
            self.shape_output.extend(path_set)
        '''
        for crossroad_point in all_paths.keys():
            for path in all_paths[crossroad_point]:
                #print("cross",crossroad_point)
                if path not in used_path:
                    #print("path",path)
                    self.build_spline(path)


    def get_sub_paths(self, base_point):
        #print("get_sub_paths",base_point)
        all_points = self.all_points
        path_s_second_point = self.path_s_second_point
        all_paths = self.all_paths

        for second_point in all_points[base_point]:
            #print("second_point",second_point)
            if second_point not in path_s_second_point[base_point]:
                #print("second_point not in path_s_second_point[base_point]")
                path_s_second_point[base_point].add(second_point)
                new_path = [base_point]
                next_point = second_point

                while len(all_points[next_point].difference(new_path)) == 1 and next_point!=base_point:
                    #print("just 2",next_point)
                    new_path.append(next_point)
                    point_set = all_points[next_point]
                    for point in point_set:
                        if point not in new_path:
                            next_point = point
                new_path.append(next_point)
                if len(new_path)>2 and base_point in all_points[next_point]:
                    new_path.append(base_point)
                all_paths[base_point].add(tuple(new_path))

                if new_path[-2] not in path_s_second_point[new_path[-1]]:
                    new_path_reversed = list(reversed(new_path))
                    all_paths[next_point].add(tuple(new_path_reversed))
                    path_s_second_point[new_path_reversed[0]].add(new_path_reversed[1])


    def build_spline2(self, path):
        used_path = self.used_path
        shape_output = self.shape_output
        all_paths = self.all_paths

        used_path.add(path)
        first = path[0]
        new_spline = list()
        new_spline.extend(path)
        next_cross_point = new_spline[-1]
        counter = 0
        while next_cross_point != first and counter<100:
            counter += 1
            next_path = self.filter_path_to_go(path, all_paths[next_cross_point])
            new_spline.extend(next_path[1:])
            next_cross_point = new_spline[-1]
            used_path.add(next_path)
        shape_output.append(new_spline)

    def build_spline(self, path):
        #print("starting new path")
        used_path = self.used_path
        shape_output = self.shape_output
        all_paths = self.all_paths

        used_path.add(path)
        first = path[0]
        next_path = path
        new_spline = list()
        new_spline.extend(path)
        next_cross_point = next_path[-1]
        counter = 0
        while next_path is not None and next_cross_point != first and counter<100:
            counter += 1
            next_path = self.filter_path_to_go(new_spline, all_paths[next_cross_point])
            #print("next path",next_path)
            if next_path is not None:
                new_spline.extend(next_path[1:])
                next_cross_point = new_spline[-1]
                used_path.add(next_path)

        #if new_spline[-1]==new_spline[0]:
            #print("equal",new_spline[-1],new_spline[0])
        shape_output.append(new_spline)
        #else:
            #print("not equal",new_spline[-1],new_spline[0])

        #print("builded:: ",new_spline)

    def filter_path_to_go(self, current_path, path_set):
        current_path_bis = current_path[1:]
        m_path = [path for path in path_set if path not in self.used_path]
        m_path = [path for path in path_set if len(set(path).intersection(current_path_bis))==0]

        m_path = [(path,get_angle(current_path[-1], current_path[-2], path[1])) for path in m_path if path!=current_path]
        m_path = [(path,angle) for path,angle in m_path if 359.5>angle>0.5]

        if len(m_path)==0:
            return None
        return min(m_path, key=itemgetter(1))[0]
