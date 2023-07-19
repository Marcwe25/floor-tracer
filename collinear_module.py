from collections import defaultdict
from itertools import combinations, permutations, product
from pprint import pprint
from vector_module import are_collinear,point_between_points
import my_utility_module as util
from timeit import default_timer as timer


def set_of_touching_segment(segment_k, dict_segment_set):
    if -1 in dict_segment_set[segment_k]:
        return None
    touching_segment_set = set()
    touching_segment_set.update({segment_k})
    searching_set = dict_segment_set[segment_k].difference(touching_segment_set)
    dict_segment_set[segment_k].clear()
    while len(searching_set) > 0:
        touching_segment_set.update(searching_set)
        acqired_set = set()
        for v in searching_set:
            acqired_set.update(dict_segment_set[v])
            dict_segment_set[v] = {-1}
        searching_set.update(acqired_set)
        searching_set.difference_update(touching_segment_set)

    return touching_segment_set


def maybe_touching(seg1, seg2):
    are_touching = point_between_points(seg1[0], seg1[1], seg2[0], 1e-02)
    if not are_touching:
        are_touching = point_between_points(seg1[0], seg1[1], seg2[1], 1e-02)
    if not are_touching:
        are_touching = point_between_points(seg2[0], seg2[1], seg1[1], 1e-02)
    return are_touching


def separate_segments_by_continuity(collinear_dict, collinear_threshold):
    segments_set_list = [set_of_touching_segment(segment_as_key, collinear_dict) for segment_as_key in
                         collinear_dict.keys()]
    segments_set_list = [x for x in segments_set_list if x is not None and -1 not in x]

    # print("separated " + str(segments_set_list))
    return segments_set_list


def check_for_segment_continuity(collinear_dict, translate_threshold):
    start1 = timer()
    separated = separate_segments_by_continuity(collinear_dict, translate_threshold)

    start2 = timer()
    # print("check_for_segment_continuity " + str(start2-start1))
    # print("check_for_segment_continuity " + str(separated))

    return separated


def segments_pair_colineare(segment_1, segment_2, collinear_threshold):
    collinear_1 = are_collinear(segment_1[0], segment_1[1], segment_2[0], collinear_threshold)
    collinear_2 = are_collinear(segment_1[0], segment_1[1], segment_2[1], collinear_threshold)
    if collinear_1 and collinear_2:
        return True
    else:
        collinear_1 = are_collinear(segment_2[0], segment_2[1], segment_1[0], collinear_threshold)
        collinear_2 = are_collinear(segment_2[0], segment_2[1], segment_1[1], collinear_threshold)
        return collinear_1 and collinear_2


def check_collinearity_v1(shapes, collinear_segment_dict, collinear_threshold):
    for segment_pair in combinations(collinear_segment_dict.keys(), 2):
        segment_1 = segment_pair[0]
        segment_2 = segment_pair[1]
        if shapes.colinear_angle(segment_1[2], (segment_2[2])):
            if util.same_space(segment_1, segment_2, collinear_threshold * 3):
                if segments_pair_colineare(segment_1, segment_2, collinear_threshold):
                    collinear_segment_dict[segment_1].add(segment_2)
                    collinear_segment_dict[segment_2].add(segment_1)
    return collinear_segment_dict


def index_collinear_segments(shapes, collinear_threshold):
    start1 = timer()
    collinear_segment_dict = defaultdict(set)
    for ishape in range(len(shapes.points)):
        for ispline in range(len(shapes.points[ishape])):
            for iknot in range(len(shapes.points[ishape][ispline]) - 1):
                segment = (shapes.get_point((ishape, ispline, iknot)), shapes.get_point((ishape, ispline, iknot + 1)),
                           shapes.get_angle_for_index((ishape, ispline, iknot))%180)
                collinear_segment_dict[segment]
            if shapes.is_closed((ishape, ispline)):
                iknot = len(shapes.points[ishape][ispline]) - 1
                segment = (shapes.get_point((ishape, ispline, iknot)), shapes.get_point((ishape, ispline, 0)),
                           round(shapes.get_angle_for_index((ishape, ispline, iknot)),0)%180)
                collinear_segment_dict[segment]

    # start2 = timer()
    # print("co 1 : " + str(collinear_segment_dict.keys()))
    # print("colinear first index " + str(start2 - start1))

    collinear_dict = check_collinearity_v1(shapes, collinear_segment_dict, collinear_threshold)

    start3 = timer()
    # print("check_colinearity_v1 " + str(start3 - start2))

    # start4 = timer()
    # print("collinear last disjoint " + str(start4 - start3))

    return collinear_dict


def get_collinear_segments(shapes, translate_threshold, collinear_threshold):
    timer1 = timer()
    collinear_dict = index_collinear_segments(shapes, collinear_threshold)
    collinear_segments = check_for_segment_continuity(collinear_dict, collinear_threshold)
    collinear_segments = [x for x in collinear_segments if len(x) > 0]
    timer2 = timer()
    print("grouping colinear point took " + str(timer2 - timer1))
    return collinear_segments
