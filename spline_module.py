class SplinePath:

    def __init__(self,spline):
        if isinstance(spline,list):
            self.spline_list = spline
        else:
            self.spline_list = list(spline)

        if isinstance(spline,set):
            self.spline_set = spline
        else:
            self.spline_set = set(spline)

    def __eq__(self, spline_other):
        if spline_other is None:
            return False
        if not isinstance(spline_other, SplinePath):
            return False
        if self.spline_set==spline_other.spline_set:
            return True
        return False

    def __ne__(self, spline_other):
        if spline_other is None:
            return True
        if not isinstance(spline_other, SplinePath):
            return True
        if self.spline_set==spline_other.spline_set:
            return False
        return True

    def __hash__(self):
        return 1
