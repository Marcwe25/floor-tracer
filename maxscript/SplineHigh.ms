
fn knotArrayToShape knotsArray closedArray = (
    ----print ("starting new shape object")
    ----print (knotsArray as string)
    outputShape = splineShape()
    for ishape = 1 to knotsArray.count where (knotsArray[ishape]!=undefined) do (
        ----print ("shape " + ishape as string)
        for ispline = 1 to knotsArray[ishape].count where(knotsArray[ishape][ispline]!=undefined and knotsArray[ishape][ispline].count>1) do (
            ----print ("spline " + ispline as string)
            splineIndex = addNewSpline outputShape
            for iknot = 1 to knotsArray[ishape][ispline].count where (knotsArray[ishape][ispline][iknot]!=undefined) do (
                addKnot outputShape splineIndex #corner #line knotsArray[ishape][ispline][iknot]
            )
            if closedArray[ishape][ispline] then close outputShape splineIndex
            updateShape outputShape
            ----print (" output spline number " + ishape as string)

        )
    )
    outputShape
)

fn knotArrayToShapeArray knotsArray  closedArray = (
    ----print ("starting new shape array")
	shapeArray = #()
    for ishape = 1 to knotsArray.count do (
		shapeArray[ishape] = splineShape()
        for ispline = 1 to knotsArray[ishape].count do (
            splineIndex = addNewSpline shapeArray[ishape]
            for iknot = 1 to knotsArray[ishape][ispline].count do (
                addKnot shapeArray[ishape] splineIndex #corner #line knotsArray[ishape][ispline][iknot]
            )
            if closedArray[ishape][ispline] then close outputShape splineIndex
            updateShape shapeArray[ishape]
            ----print (" output spline number " + ishape as string)
        )
    )
    shapeArray
    )
    
