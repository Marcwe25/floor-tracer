from collections import defaultdict
from itertools import chain
from math import fabs
from point_module import Point
from my_utility_module import isclose
from vector_module import get_angle

class Corrector_primary:
    def __init__(self, shape):
        self.shape=shape
        self.backup_e = Point.e

    def make_primary_correction(self,e):
        #self.shape.remove_consecutive_duplicate_point()
        self.shape.reassign_e(e)
        self.shape.rebuild_all_index()
        self.scan_point_to_unify()
        self.shape.reassign_e(self.backup_e)

    def scan_point_to_unify(self):
        shape = self.shape
        scanned_point = set()
        for x_key in shape.index.keys():
            for y_keys in shape.index[x_key].keys():
                #print_segmentsprint(x_key,y_keys,"--------------============++++++++++++kkkkkkkkkk++++++++-------")
                conn_segments = shape.connected_segment_index_angle_from_index_by_e(x_key,y_keys)
                #print("conn_segments",conn_segments)
                #self.print_segments(conn_segments)
                angle_dict = self.angle_dict_counter (conn_segments)
                #for k in angle_dict.keys():
                #    #print("angle dict",k,angle_dict[k])
                #print("len(angle_dict)==2",len(angle_dict)==2)
                if len(angle_dict)==2:
                    angles = list(angle_dict.keys())
                    #print("list of angles",angles)
                    for angle in angles:
                        if angle>360:
                            angle[0]=angle[0]/0
                    #print("fabs(fabs(angles[0]-angles[1])-180)<shape.angle_precision",fabs(fabs(angles[0]-angles[1])-180)<shape.angle_precision)
                    if fabs(fabs(angles[0]-angles[1])-180)<shape.angle_precision:
                        closest_0 = shape.get_point(min(angle_dict[angles[0]],key=self.segment_length)[1])
                        closest_180 = shape.get_point(min(angle_dict[angles[1]],key=self.segment_length)[1])
                        pos_dict = defaultdict(set)
                        for a in angle_dict.keys():
                            for s in angle_dict[a]:
                                sp = (self.shape.get_point(s[0]),self.shape.get_point(s[1]),s[2])
                                pos_dict[a].add(sp)
                            #print("pos_dict",a,pos_dict[a])

                        min_180 = min(angle_dict[angles[1]],key=self.segment_length)
                        min_0 = min(angle_dict[angles[0]],key=self.segment_length)
                        #print("min_180",min_180)
                        #print("min_0",min_0)
                        #print("closest_0",closest_0)
                        #print("closest_180",closest_180)
                        for segment in angle_dict[angles[0]]:
                            #print("eee",segment,segment[0][2],segment[1][2])
                            if segment[0][2]>segment[1][2]:
                                seg = self.shape.get_segment(segment[0])
                                if seg is None:
                                    #print("seg1")
                                    shape.get_point(segment[0]).set_position(closest_180.get_position())
                                else:
                                    #print("seg2")
                                    shape.get_point(segment[0]).set_position(shape.get_point(seg[1]).get_position())
                            else:
                                seg = self.shape.prev_segment(segment[0],True)
                                if seg is None:
                                    #print("seg3")
                                    shape.get_point(segment[0]).set_position(closest_180.get_position())
                                else:
                                    #print("seg4",segment[0],shape.get_point(segment[0]),"to",shape.get_point(seg[0]).get_position())
                                    #point_0 = shape.get_point(segment[0])
                                    #point_1 = shape.get_point(seg[0])
                                    #print("p0x",point_0.x)
                                    #print("p0xe",point_0.xe)
                                    #point_0.x = point_1.x
                                    #point_0.y = point_1.y
                                    #print("p0x",point_0.x)
                                    #print("p0xe",point_0.xe)
                                    shape.get_point(segment[0]).set_position(shape.get_point(seg[0]).get_position())

                        for segment in angle_dict[angles[1]]:
                            if segment[0][2]>segment[1][2]:
                                seg = self.shape.get_segment(segment[0])
                                if seg is None:
                                    #print("seg5")
                                    shape.get_point(segment[0]).set_position(closest_0.get_position())
                                else:
                                    #print("seg4",segment[0],shape.get_point(segment[0]),"to",shape.get_point(seg[1]).get_position())
                                    #point_0 = shape.get_point(segment[0])
                                    #point_1 = shape.get_point(seg[1])
                                    #point_0.x = point_1.x
                                    #point_0.y = point_1.y
                                    shape.get_point(segment[0]).set_position(shape.get_point(seg[1]).get_position())
                            else:
                                seg = self.shape.prev_segment(segment[0],True)
                                if seg is None:
                                    #print("seg7")
                                    shape.get_point(segment[0]).set_position(closest_0.get_position())
                                else:
                                    #print("seg8")
                                    shape.get_point(segment[0]).set_position(shape.get_point(seg[0]).get_position())


    def angle_dict_counter (self, segments):
        shape=self.shape
        angle_dict = defaultdict(set)
        for segment in segments:
            found = False
            for angle_key in angle_dict.keys():
                if shape.same_angle(angle_key,segment[2]):
                    found=True
                    angle_dict[angle_key].add(segment)
            if not found:
                angle_dict[segment[2]].add(segment)
        return angle_dict

    def segment_length(self, segment):
        return self.shape.get_point(segment[0]).distance(self.shape.get_point(segment[1]))

    def print_segments(self,segments):
        sps = []
        for segment in segments:
            s = (self.shape.get_point(segment[0]),self.shape.get_point(segment[1]),segment[2])
            sps.append(s)
        #print(sps)
