from timeit import default_timer as timer

import max_module
from contour_module import ContourTracer
import corrector_module
from corrector_primary import Corrector_primary
from general_cache_module import AngleCache
from interior_module import InternalBuilder
from intersection_module import flow_add_intersection
from shape_module import Shapes


def run_flow(shape_input):
    total_timer_start = timer()
    time_start = timer()
    shape = Shapes()
    shape.add_points_data(shape_input[0],shape_input[1])
    shape.build_index("first")
    AngleCache.shape=shape
    time_end = timer()
    print("build shape data took " + str(time_end-time_start))

    prim_corrector = Corrector_primary(shape)
    prim_corrector.make_primary_correction(0.5)
    #max_module.shape_array_to_shape_object(shape.points, shape.isClosed, "primary correction")

    shape.rebuild_all_index()
    time_start = timer()
    corrector = corrector_module.CorrectorSimple(shape)
    corrector.do_correction()
    time_end = timer()
    #max_module.shape_array_to_shape_object(shape.points, shape.isClosed, "correction")
    print("corrector took " + str(time_end-time_start))

    shape.rebuild_all_index()
    time_start = timer()
    flow_add_intersection(shape)
    time_end = timer()
    print("add_intersection took " + str(time_end-time_start))
    #max_module.shape_array_to_shape_object(shape.points, shape.isClosed, "intersection")

    time_contour_start = timer()
    shape.rebuild_all_index()
    contour_tracer = ContourTracer(shape)
    contour_data = contour_tracer.draw_contour()
    #max_module.shape_array_to_shape_object([[contour_data]], [[True]],"contour")
    time_contour_end = timer()
    print("tracing contour took " + str(time_contour_end-time_contour_start))


    shape.rebuild_all_index()

    time_internal_start = timer()
    internal_builder = InternalBuilder(shape,contour_data)
    internal_builder.build_interior()
    time_internal_end = timer()
    print("tracing internal region took " + str(time_internal_end-time_internal_start))

    internal_data = internal_builder.get_output()

    internal_close = [True]*len(internal_data)
    max_module.shape_array_to_shape_object([internal_data],[internal_close], "internal")

    total_timer_end = timer()
    print("all calculation took " + str(total_timer_end-total_timer_start))
