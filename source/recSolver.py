#!/usr/bin/python

import sys
import solution_closed_form



if sys.argv[1:] is ['-version']:
	print "1.0"

if sys.argv[1:] != [] and sys.argv[-1] is not None:
	expression = sys.argv[-2]
        variable = sys.argv[-1]	
	if len(sys.argv[1:])==2: 
		solution_closed_form.solve_recurrence(expression,variable)
	else:
		print "Wrong options"

