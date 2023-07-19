import MaxPlus
from itertools import chain

from point_module import Point


def shape_array_to_shape_object(shape_array, close_array, nodeName = "default"):
    obj = MaxPlus.Factory_CreateShapeObject(MaxPlus.ClassIds.SplineShape)
    shape = MaxPlus.SplineShape__CastFrom(obj)

    bezier = shape.GetShape()
    bezier.NewShape()

    for ishape, oshape in enumerate(shape_array):
        for ispline, ospline in enumerate(oshape):
            spline = bezier.NewSpline()
            for oknot in ospline:
                p = MaxPlus.Point3(oknot.x, oknot.y, 0)
                spline.AddKnot(
                    MaxPlus.SplineKnot(MaxPlus.SplineKnot.CornerKnot, MaxPlus.SplineKnot.LineLineType, p, p, p))
            spline.SetClosed(close_array[ishape][ispline])

    bezier.UpdateSels()
    bezier.InvalidateGeomCache()
    node = MaxPlus.Factory.CreateNode(obj, nodeName)

def set_of_segment_to_shape(set_of_segment,isclose, nodeName = "default"):
    points_set = {p for p in chain(*set_of_segment) if isinstance(p,Point)}
    point_list = list(points_set)
    shape_array_to_shape_object([[point_list]],[[isclose]], nodeName)
    pass
