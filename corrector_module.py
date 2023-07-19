from collections import defaultdict
from itertools import chain

import collinear_module
import my_utility_module as util
import point_module
import vector_module
from vector_module import point_line_distance, closest_point_on_line


class CorrectorSimple:

    translate_threshold=3
    collinear_threshold=3

    def __init__(self, shapes, translate_threshold=4, collinear_threshold=4):
        self.shapes = shapes
        #print("sssss1",self.shapes.points)
        CorrectorSimple.translate_threshold = translate_threshold
        CorrectorSimple.collinear_threshold = collinear_threshold
        self.translate_threshold = CorrectorSimple.translate_threshold
        self.collinear_threshold = CorrectorSimple.collinear_threshold

    def stronger_by_segment_length(self, point_cluster):
        # print("point cluster " ,point_cluster )
        biggest_length = 0
        wining_point = None
        for p in point_cluster:
            # print("for pointttt",p,self.shapes.get_point(p))
            seg = self.shapes.get_segment(p)
            preview_segment = self.shapes.prev_segment(p, True)
            # print("segment" , seg, preview_segment)
            # print()
            for segment in {seg, preview_segment}:
                if segment is not None:
                    p1 = self.shapes.get_point(segment[0])
                    p2 = self.shapes.get_point(segment[1])
                    d = p1.distance(p2)
                    # print("distance ", p1 ,p2 ,d)
                    if d > biggest_length:
                        biggest_length = d
                        wining_point = p

        return wining_point



    def correct_points_to_points(self):
        for x_key in self.shapes.index.keys():
            for y_key in self.shapes.index[x_key]:
                point_index_set = self.shapes.index[x_key][y_key]
                #print("point index set is " , point_index_set)
                if len(point_index_set) >= 1:
                    point_1_index = util.get_from_set(point_index_set)
                    #print("point 1 index is ", point_1_index)
                    point_1 = self.shapes.get_point(point_1_index)
                    #print("point 1 is ",point_1)
                    if point_1 is not None:
                        point_cluster = self.shapes.get_from_index(point_1)
                        if len(point_cluster) > 1:
                            strongest_point = self.stronger_by_segment_length(point_cluster)
                            the_point = self.shapes.get_point(strongest_point)
                            #print("moving to " + str(the_point))
                            if strongest_point is not None:
                                self.shapes.move_cluster(the_point,
                                                         self.shapes.get_point(strongest_point).get_position())

    def search_correction(self, collinear_segments):
        correction_table = defaultdict(point_module.Point)
        for i, segment_set in enumerate(collinear_segments):
            direction_test_segment = util.get_from_set(segment_set)
            # print("direction by " + str(direction_test_segment))
            vector_module.set_point_direction(direction_test_segment)
            old_e = point_module.Point.e
            # PointModule.Point.e = 0.001
            points_set = {p for p in chain(*segment_set) if isinstance(p, point_module.Point)}
            # print("before sort " + str(points_set))
            points_set = sorted(points_set)
            #print("after sort " + str(points_set))
            # print("collinear " + str(i) + " " + str(points_set))
            #shape_array_to_shape_object([[points_set]], [[False]], str("collinear" + str(i)))
            start = points_set[0]
            end = points_set[-1]
            # print("col set " + str(points_set))
            # print("col set " + str(segment_set))
            # print("start " + str(start))
            # print("end " + str(end))
            middle_set = points_set[1:-1]
            #print("search correction for", points_set)
            for p in middle_set:
                distance_to_main_segment = point_line_distance(start, end, p)
                if distance_to_main_segment >= 0:
                    potential_target = set()
                    points_cluster = self.shapes.get_from_index(p)
                    for point_index_from_cluster in points_cluster:
                        preview_segment = self.shapes.prev_segment(point_index_from_cluster, True)
                        next_segment = self.shapes.get_segment(point_index_from_cluster)
                        for the_segment in [preview_segment, next_segment]:
                            if the_segment is not None:
                                point_1 = self.shapes.get_point(the_segment[0])
                                point_2 = self.shapes.get_point(the_segment[1])
                                intersection_with_the_segment = vector_module.get_intersection(start, end, point_1,point_2, False)
                                if intersection_with_the_segment is not None and intersection_with_the_segment.z!=100:
                                    potential_target.add(intersection_with_the_segment)
                                    #print("new intersection 1" + str(start) + " " + str(end) + " " + str(point_1) + " " + str(point_2) + " " +str(intersection_with_the_segment))
                    # print("target for " + str(p))
                    # for x in potential_target:
                    #    #print(x)
                    # print(".............")
                    potential_target = set(
                        filter(lambda x: (p.distance(x) < self.translate_threshold), potential_target))
                    if len(potential_target) == 0:
                        closest_target = closest_point_on_line(start, end, p)
                        #print("closest target from",start,end,p,closest_target)
                        #print("p",p)
                        #print("closest_target",closest_target)
                        #print("distance ", closest_target.distance(p))
                        #print("thtrs",self.translate_threshold)
                        if closest_target.distance(p) < self.translate_threshold:
                            correction_table[p] = closest_target
                            #print("added closest_target " + str(start) + " " + str(end) + " " +str(closest_target))

                    else:
                        closest_target = min(potential_target, key=lambda x: x.distance(p))
                        if closest_target.distance(p) < self.translate_threshold:
                            correction_table[p] = closest_target
                            #print("added closest intersection 2" + str(start) + " " + str(end) + " " +str(closest_target))
                    #print("moving colinear ", p , correction_table[p])
                    # print("*********")

            point_module.Point.e = old_e
        return correction_table

    def make_move_from_correction_table(self, correction_table):
        for k in correction_table.keys():
            self.shapes.move_cluster(k, correction_table[k].get_position())

    def do_correction(self):
        self.shapes.remove_consecutive_duplicate_point()
        self.shapes.build_index("corr1")
        self.correct_points_to_points()

        self.shapes.rebuild_all_index()
        collinear_segments = collinear_module.get_collinear_segments(self.shapes, self.translate_threshold, self.collinear_threshold)
        correction_table = self.search_correction(collinear_segments)
        self.make_move_from_correction_table(correction_table)

