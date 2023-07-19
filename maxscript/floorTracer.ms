
rollout floorTracer "Trace Floor 5" width:266 height:329
(
--------------------------------------- structure --------------------------------------------
    include "C:/Users/happyCouple/Google Drive/maxscript/onlineFloorTracer5/mwsshapedata.ms"

	--------------------------------------- VARIABLE --------------------------------------------

	local splineInput = #()
	local initialData
	local indx
	local contour
	local minWallWith
	local maxWallWidth = 40
	local bridgeEmptyWindows = true

--------------------------------------- UI ELEMENT --------------------------------------------

	button processButton "create" pos:[176,228] width:75 height:24

--------------------------------------- Files --------------------------------------------
    include "C:/Users/happyCouple/Google Drive/maxscript/onlineFloorTracer5/py_convert.ms"
    include "C:/Users/happyCouple/Google Drive/maxscript/onlineFloorTracer5/SplineHigh.ms"
	include "C:/Users/happyCouple/Google Drive/maxscript/onlineFloorTracer5/modifierFactory.ms"
	
	include "C:/Users/happyCouple/Google Drive/maxscript/runner_5/1/flow.ms"
	
------------------------------------------ UI EVENT --------------------------------------------



	on processButton pressed do (
        splineInput = ($selection as array)
		InitializeScriptData()
	)


)
createdialog floorTracer
