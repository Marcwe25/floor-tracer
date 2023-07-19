local runner = undefined


fn runPythonCode data = (
  runner.run data
  print "python done with"
)

fn InitializeScriptData  = (
  local sys = python.import("sys")
  while sys.path.__contains__ py_path do (
    sys.path.remove py_path
  )
  sys.path.insert 1 py_path
	
  runner = python.Import("runner_module")
  
  initialData = shapeDataStructure shapeArray:splineInput
  data = #(initialData.kposition,initialData.kisClosed)
  runPythonCode data
)
