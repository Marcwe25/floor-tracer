import my_utility_module as util

def correct_points_to_points(shape):
    for x_key in shape.index.keys():
        for y_key in shape.index[x_key]:
            point_index_set = shape.index[x_key][y_key]
            #print("point index set is " , point_index_set)
            if len(point_index_set) >= 1:
                point_1_index = util.get_from_set(point_index_set)
                #print("point 1 index is ", point_1_index)
                point_1 = shape.get_point(point_1_index)
                #print("point 1 is ",point_1)
                if point_1 is not None:
                    point_cluster = shape.get_from_index(point_1)
                    if len(point_cluster) > 1:
                        strongest_point = stronger_by_segment_length(shape,point_cluster)
                        the_point = shape.get_point(strongest_point)
                        #print("moving to " + str(the_point))
                        if strongest_point is not None:
                            shape.move_cluster(the_point,
                                                     shape.get_point(strongest_point).get_position())

def stronger_by_segment_length(shape,point_cluster):
    # print("point cluster " ,point_cluster )
    biggest_length = 0
    wining_point = None
    for p in point_cluster:
        # print("for pointttt",p,shape.get_point(p))
        seg = shape.get_segment(p)
        preview_segment = shape.prev_segment(p, True)
        # print("segment" , seg, preview_segment)
        # print()
        for segment in {seg, preview_segment}:
            if segment is not None:
                p1 = shape.get_point(segment[0])
                p2 = shape.get_point(segment[1])
                d = p1.distance(p2)
                # print("distance ", p1 ,p2 ,d)
                if d > biggest_length:
                    biggest_length = d
                    wining_point = p

    return wining_point
