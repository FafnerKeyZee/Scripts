#!/usr/bin/python
#
# Decode VBA Macro based on chr() obfuscation
# Xavier Mertens <xavier@rootshell.be>
#

#
# Modified version, original is there : 
# https://github.com/xme/toolbox/blob/master/deobfuscate_chr.py
#

"
import re
import sys

def do_chr(m):
	if m.group(0):
		return eval(re.sub(r'[cC][hH][rR][wW\$]*\(([\d\+\-\s.]*)\)',r'chr(int(\1))', m.group(0)))	
	return ""
	
f = open(sys.argv[1], 'rb')
for line in f.readlines():
	line = re.sub(r'[cC][hH][rR][wW\$]*\(([\d+\+\-\s\.]*)\)', do_chr, line)
	line = re.sub(" & ", "", line)
	print line.rstrip()
f.close()
exit
