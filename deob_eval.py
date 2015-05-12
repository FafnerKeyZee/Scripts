#!/usr/bin/python
#
# Decode VBA Macro based on this obfuscator 
# https://github.com/kkar/VBS-Obfuscator-in-Python
#
# Fafner [_KeyZee_]
#

import re
import sys
	
for line in sys.stdin.readlines():
        decoded = ""
        line = line.rstrip()
        encoded = line.split('*')
        if (len(encoded)> 1):
		for i in range(0, len(encoded) ):
			decoded+=chr(eval(encoded[i]))
	print decoded
exit
