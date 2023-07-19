import sys


def run(shape_input):
    my_modules = ["CollinearSetModule", "Contour_Module", "CorrectorSimpleModule", "dataUtility", "flow_py",
                  "Intersection_module","intersection_runner", "mathUtility", "MyUtilityModule", "PointModule", "ShapeModule",
                  "Vector_Module", "maxModule"]

    my_modules2 = ["collinear_module", "contour_module", "corrector_module", "data_utility_module", "flow_py_module",
                  "internal_builder","intersection_module", "my_utility_module", "point_module", "shape_module",
                  "vector_module", "max_module","interior_module","internal_path_module","general_cache_module","corrector_primary"]

    for module in my_modules:
        if module in sys.modules:
            print("deleting modules",module)
            del sys.modules[module]

    for module in my_modules2:
        if module in sys.modules:
            del sys.modules[module]

    import flow_py_module
    flow_py_module.run_flow(shape_input)
    module = "runner_module"
    if module in sys.modules:
            del sys.modules[module]

'''
    shape_input = [[[(-10786.3, -753.3, 0), (-10786.3, -1133.3, 0), (-10766.3, -1133.3, 0), (-10766.3, -753.3, 0)],
                     [(-10386.3, -733.3, 0), (-10786.3, -733.3, 0), (-10786.3, -753.3, 0), (-10386.3, -753.3, 0)],
                     [(-10386.3, -1133.3, 0), (-10386.3, -753.3, 0), (-10406.3, -753.3, 0), (-10406.3, -1133.3, 0)],
                     [(-10766.3, -1133.3, 0), (-10406.3, -1133.3, 0), (-10406.3, -1113.3, 0), (-10766.3, -1113.3, 0)]],
                   [True, True, True, True]]
'''
