#!/usr/bin/python

import sys
import input_files



if sys.argv[1:] is ['-version']:
	print "1.0"

if sys.argv[1:] != [] and sys.argv[-1] is not None and sys.argv[-2] is not None:
        file_name1 = sys.argv[-1]
	file_name2 = sys.argv[-2]
	if len(sys.argv[1:])==2: 
		input_files.find_equiv(file_name1,file_name2)	
	else:

		input_files.find_equiv(None,None)


