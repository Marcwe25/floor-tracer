
rollout floorTracer "Trace Floor 5" width:266 height:329
(
--------------------------------------- structure --------------------------------------------
	local user_path = systemTools.getEnvVariable("USERPROFILE")
	local my_script_path = user_path + "/Google Drive/maxscript/onlineFloorTracer5/"
	local py_path = user_path + "/Google Drive/pythonMax/pr6/"
	local ddd = my_script_path+"mwsshapedata.ms"
	include ddd

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
    include my_script_path+"py_convert.ms"
    include my_script_path+"SplineHigh.ms"
	include my_script_path+"modifierFactory.ms"
	include py_path+"localFloor/flow.ms"

------------------------------------------ UI EVENT --------------------------------------------



	on processButton pressed do (
        splineInput = ($selection as array)
		InitializeScriptData()
	)


)
createdialog floorTracer
