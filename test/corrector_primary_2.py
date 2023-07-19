from collections import defaultdict
from itertools import chain
from math import fabs

from my_utility_module import isclose
from vector_module import get_angle


def make_primary_correction(shape):
    shape.remove_consecutive_duplicate_point()
    shape.set_full_spline_segment_array(True)


def unify_at_index(circuits,shape,segment):
    p1 = shape.get_point(segment[1])

    conn_seg = shape.get_seg_from_index(p1)
    pre_seg = shape.pre_seg_from_index(p1)
    if len(conn_seg)+len(pre_seg)>1:
        conn_seg_points = [(shape.get_point(seg[0]),shape.get_point(seg[1])) for seg in conn_seg]
        pre_seg_points = [(shape.get_point(seg[0]),shape.get_point(seg[1])) for seg in pre_seg]
        club_0 = {}
        club_180 = {}


def unify_vertices(shape):
    circuits = defaultdict(set)
    for ishape,_ in enumerate(shape.points):
        for ispline,_ in enumerate(shape.points[ishape]):
            for iknot in range(1,len(shape.points[ishape][ispline])):
                unify_at_index(circuits,shape,(ishape,ispline,iknot))

                p1 = shape.get_point((ishape,ispline,iknot))
                conn_seg = shape.get_seg_from_index(p1)
                conn_seg_points = [(shape.get_point(seg[0]),shape.get_point(seg[1])) for seg in conn_seg]
                pre_seg = shape.pre_seg_from_index(p1)
                pre_seg_points = [(shape.get_point(seg[0]),shape.get_point(seg[1])) for seg in pre_seg]

                if len(conn_seg)+len(pre_seg)>1:
                    reference_segment =
                    ip2 = None
                    for ipo, opo in enumerate(points_inst):
                        if opo != p1:
                            ip2 = ipo
                            break
                    all_collinears = True
                    club_0 = set()
                    club_180 = set()
                    for ipo,opo in enumerate(points_inst):
                        angle = get_angle(p1,p2,po)
                        if isclose(angle,180,abs_tol=1):
                            club_180.add((p2,po))
                        elif isclose(angle,360,abs_tol=1) or isclose(angle,0,abs_tol=1):
                            club_0.add((p2,po))
                        else:
                            all_collinears = False
                            break

                        if all_collinears and len(club_180)>0:
                            circuits[p1].update(club_180)


def scan_point_to_unify2(shape):
    scanned_point = set()
    spline_to_delete = set()
    for ishape,_ in enumerate(shape.points):
        for ispline,_ in enumerate(shape.points[ishape]):
            if len(shape.points[ishape][ispline]<2):
                spline_to_delete.add((ishape,ispline))
            else:
                if shape.is_closed((ishape,ispline)) and len(shape.points[ishape][ispline])==2:
                    shape.isClosed[ishape][ispline] = False
                if shape.is_closed((ishape,ispline)):
                    for iknot in enumerate(shape.points[ishape][ispline]):
                        scanned_point.add((ishape,ispline,iknot))
                else:
                    spline_last_segment = (shape.points[ishape][ispline][-2:],shape.get_closest_angle((ishape,ispline,-2)))
                    spline_first_segment = (reversed(shape.points[ishape][ispline][:2]), shape.get_closest_reverse_angle((ishape,ispline,0)))
                    for segment in (spline_first_segment,spline_last_segment):
                        point_instance = shape.get_point(segment[0][1])
                        point_angle_connection = shape.connected_segment_index_closest_angle_from_index(point_instance)
                        all_collinear = True
                        for _,_,angle in point_angle_connection:
                            if not shape.same_angle(angle,segment[1]):
                                all_collinear = False
                                break
                        if all_collinear:
                            inbound_angle = 0
                            if segment is spline_last_segment:
                                inbound_angle = shape.get_angle_for_index(segment[0])
                            else:
                                inbound_angle = shape.get_angle_for_index(segment[1])

                            connection_segment = shape.connected_segment_index_angle_from_index(point_instance)
                            spline_angle_centric = defaultdict(set)
                            for segment in connection_segment:
                                if not shape.same_angle(segment[2],inbound_angle):
                                    spline_angle_centric[180].add(segment)
                                else:
                                    spline_angle_centric[0].add(segment)
                            for segment in spline_angle_centric[0]:
                                if shape.points[segment[0][0]][segment[0][1]][-1] != point_instance:
                                    shape.points[segment[0][0]][segment[0][1]].reverse()
                                del shape.points[segment[0][0]][segment[0][1]][-1]
                            for segment in  spline_angle_centric[180]:
                                if shape.points[segment[0][0]][segment[0][1]][0] != point_instance:
                                    shape.points[segment[0][0]][segment[0][1]].reverse()
                                del shape.points[segment[0][0]][segment[0][1]][0]
                            for segment_start in spline_angle_centric[0]:
                                for segment_end in spline_angle_centric[180]:
                                    shape.points[segment_start[0][0]][segment_start[0][1].extend(shape.points[segment_end[0][0]][segment_end[0][1])
                                    spline_to_delete.add((segment_end[0][0],segment_end[0][1]))

def scan_point_to_unify(shape):
    scanned_point = set()
    for x_key in shape.index.keys():
        for y_keys in shape[x_key].keys():
            conn_segments = shape.connected_segment_index_angle_from_index_by_e(x_key,y_keys)
            angle_dict = angle_dict_counter (conn_segments,shape)
            if len(angle_dict)==2:
                angles = list(angle_dict.keys())
                for angle in angles:
                    if angle>360:
                        angle[0]=angle[0]/0
                if fabs(fabs(angles[0]-angles[1])-180)<shape.angle_precision:
                    closest_0 = min(angle_dict[angle[0]],key=segment_lenght)
                    closest_180 = min(angle_dict[angle[1]],key=segment_lenght)
                    for segment in angle_dict[angle[0]]:


            for _,_,angle in conn_segments:
                            if not shape.same_angle(angle,segment[1]):
                                all_collinear = False
                                break
                        if all_collinear:
                            inbound_angle = 0
                            if segment is spline_last_segment:
                                inbound_angle = shape.get_angle_for_index(segment[0])
                            else:
                                inbound_angle = shape.get_angle_for_index(segment[1])

                            connection_segment = shape.connected_segment_index_angle_from_index(point_instance)
                            spline_angle_centric = defaultdict(set)
                            for segment in connection_segment:
                                if not shape.same_angle(segment[2],inbound_angle):
                                    spline_angle_centric[180].add(segment)
                                else:
                                    spline_angle_centric[0].add(segment)
                            for segment in spline_angle_centric[0]:
                                if shape.points[segment[0][0]][segment[0][1]][-1] != point_instance:
                                    shape.points[segment[0][0]][segment[0][1]].reverse()
                                del shape.points[segment[0][0]][segment[0][1]][-1]
                            for segment in  spline_angle_centric[180]:
                                if shape.points[segment[0][0]][segment[0][1]][0] != point_instance:
                                    shape.points[segment[0][0]][segment[0][1]].reverse()
                                del shape.points[segment[0][0]][segment[0][1]][0]
                            for segment_start in spline_angle_centric[0]:
                                for segment_end in spline_angle_centric[180]:
                                    shape.points[segment_start[0][0]][segment_start[0][1].extend(shape.points[segment_end[0][0]][segment_end[0][1])
                                    spline_to_delete.add((segment_end[0][0],segment_end[0][1]))

def angle_dict_counter (segments,shape):
    angle_dict = defaultdict(set)
    for segment in segments:
        for angle_key in angle_dict.keys():
            found = False
            if shape.same_angle(angle_key,segment[2]):
                found=True
                angle_dict[angle_key].add(segment)
            if not found:
                angle_dict[segment[2]].add(segment)
    return angle_dict

def segment_lenght(segment):
    return shape.get_point(segment[0]).distance(segment[1])
