fn shapeArrayFromPy data = (
    sssaaa = #()
    for ishape=1 to data.count do (
        append sssaaa #()
        print "shape"
        print (data[ishape] as string)
        for ispline = 1 to data[ishape].count do (
            print "spline"
            print (data[ishape][ispline] as string)
            append sssaaa[sssaaa.count] #()
            for iknot = 1 to data[ishape][ispline].count do (
                print "iknot"
                print (data[ishape][ispline][iknot] as string)
                p = data[ishape][ispline][iknot]
                print (ClassOf p)
                pm = [p[0],p[1],p[2]]
                print pm
                append sssaaa[ishape][ispline][iknot] pm
            )
        )
    )
    sssaaa
)