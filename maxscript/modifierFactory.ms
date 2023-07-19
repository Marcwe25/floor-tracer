fn shapeToSweepWall splineObject= (
    sweepMod = sweep ()
    addModifier splineObject sweepMod
    redrawViews() 
    sweepMod.CurrentBuiltInShape=2
    redrawViews() 
    sweepMod[4].width=20
    sweepMod[4].length=350
    sweepMod.SmoothSection=off
    sweepMod.SmoothPath=off
    sweepMod.PivotAlignment=2
    redrawViews() 
)