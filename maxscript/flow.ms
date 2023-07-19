local runner = undefined


fn runPythonCode data = (
  runner.run data
  print "python done with drawing"

)

fn InitializeScriptData  = (
  local sys = python.import("sys")
  thepath = "C:\Users\happyCouple\Google Drive\pythonMax\pr6"
  print ("using " + thepath)
  while sys.path.__contains__ thepath do (
    sys.path.remove thepath
  )
  sys.path.insert 1 thepath
	
  runner = python.Import("runner_module")
  
  initialData = shapeDataStructure shapeArray:splineInput
  data = #(initialData.kposition,initialData.kisClosed)
  runPythonCode data
)
