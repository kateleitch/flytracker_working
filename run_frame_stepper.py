from __future__ import print_function
import sys
import skytracker 

file_name = sys.argv[1]
stepper = skytracker.FrameStepper(file_name)
stepper.run()
