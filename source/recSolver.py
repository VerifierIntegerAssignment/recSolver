#!/usr/bin/python

import sys
import viap_svcomp



if sys.argv[1:] is ['-version']:
	print "1.0"

if sys.argv[1:] != [] and sys.argv[-1] is not None:
	expression = sys.argv[-2]
        variable = sys.argv[-1]	
	if len(sys.argv[1:])==2: 
		viap_svcomp.solve_recurrence(expression,variable)
	else:
		print "Wrong options"

