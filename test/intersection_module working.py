from collections import defaultdict
from itertools import chain, combinations
from timeit import default_timer as timer

import vector_module
from my_utility_module import same_space
from point_module import Point
from vector_module import point_between_points, get_intersection, point_between_points2, are_collinear, \
    closest_point_on_line_param, set_point_direction


def get_intersection_in_shape(shape, intersection_dict):
    spline_array = shape.get_spline_segment_array()
    all_segment_pair = combinations(chain(*spline_array), 2)
    intersection_tolerance = 0.12
    for point_pair in all_segment_pair:
        point_a1 = shape.get_point(point_pair[0][0])
        point_a2 = shape.get_point(point_pair[0][1])
        point_b1 = shape.get_point(point_pair[1][0])
        point_b2 = shape.get_point(point_pair[1][1])
        if same_space([point_a1, point_a2], [point_b1, point_b2], 0):
            intersection = get_intersection(point_a1, point_a2, point_b1, point_b2, False)
            if intersection is not None:
                if intersection.z == 100:
                    if point_b1 != point_a1 and point_b1 != point_a2:
                        if point_between_points2(point_a2, point_a1, point_b1, intersection_tolerance):
                            if are_collinear(point_a2, point_a1, point_b1, intersection_tolerance):
                                intersection_dict[point_pair[0][0]].add(point_b1)
                    if point_b2 != point_a1 and point_b2 != point_a2:
                        if point_between_points2(point_a2, point_a1, point_b2, intersection_tolerance):
                            if are_collinear(point_a2, point_a1, point_b2, intersection_tolerance):
                                intersection_dict[point_pair[0][0]].add(point_b2)
                    if point_b2 != point_a1 and point_b1 != point_a1:
                        if point_between_points2(point_b2, point_b1, point_a1, intersection_tolerance):
                            if are_collinear(point_b2, point_b1, point_a1, intersection_tolerance):
                                intersection_dict[point_pair[1][0]].add(point_a1)
                    if point_b2 != point_a2 and point_b1 != point_a2:
                        if point_between_points2(point_b2, point_b1, point_a2, intersection_tolerance):
                            if are_collinear(point_b2, point_b1, point_a2, intersection_tolerance):
                                intersection_dict[point_pair[1][0]].add(point_a2)
                else:
                    if intersection == point_a1:
                        print("moving a ",point_a1, " to ", intersection)
                        shape.move_cluster(point_a1, intersection.get_position())
                    else:
                        intersection_dict[point_pair[0][0]].add(intersection)

                    if intersection == point_b1:
                        print("moving b ",point_b1, " to ", intersection)
                        shape.move_cluster(point_b1, intersection.get_position())
                    else:
                        intersection_dict[point_pair[1][0]].add(intersection)


def flow_add_intersection(shape):
    intersection_dict = defaultdict(set)

    time_start = timer()
    get_intersection_in_shape(shape, intersection_dict)
    # get_intersection_in_shape     1.1898115251060517)
    time_end = timer()
    # print("get_intersection_in_shape", time_end - time_start)
    time_end = timer()
    indexes = sorted(intersection_dict.keys())
    indexes.reverse()
    time_start = timer()
    # print("1 intersection sorted ", time_start - time_end)
    for index in indexes:
        current_point = shape.get_point(index)
        next_point = shape.get_point(shape.next_point(index, True))
        # print("index1 ",index,intersection_dict[index])

        # print("index2 ",index,intersection_dict[index])
        intersections = list(intersection_dict[index]) + [current_point, next_point]
        vector_module.set_point_direction(intersections)

        intersections = sorted(intersections)
        if intersections[-1] == current_point:
            intersections.reverse()
        intersections.remove(current_point)
        intersections.remove(next_point)
        shape.points[index[0]][index[1]][index[2] + 1:index[2] + 1] = intersections
        shape.remove_consecutive_duplicate_point()
    shape.remove_consecutive_duplicate_point()
    shape.build_index("inters")


def get_extended_intersection(shape, point_a1, point_a2, error_thresold):
    intersections = defaultdict(set)
    spline_array = shape.get_spline_segment_array()
    for spline in spline_array:
        for segment in spline:
            point_b1 = shape.get_point(segment[0])
            point_b2 = shape.get_point(segment[1])
            intersection = get_intersection(point_a1, point_a2, point_b1, point_b2, True)
            if intersection is not None:
                if intersection.z == 100:
                    potential_points = {point_b1, point_b2}
                    for potential_point in potential_points:
                        if potential_point != point_a1 and potential_point != point_a2:
                            if closest_point_on_line_param(point_a1, point_a2, potential_point) > 1:
                                if are_collinear(point_a1, point_a2, potential_point, error_thresold):
                                    s = {shape.get_point(i) for i in shape.get_connected_points(potential_point, True)}
                                    intersections[potential_point].update(s)
                else:
                    if intersection != point_a1 and intersection != point_a2:
                        if closest_point_on_line_param(point_a1, point_a2, intersection) > 1:
                            if point_between_points(point_b1, point_b2, intersection, error_thresold):
                                s = {shape.get_point(i) for i in shape.get_connected_points(intersection, True)}
                                intersections[intersection].update(s)
    return intersections
