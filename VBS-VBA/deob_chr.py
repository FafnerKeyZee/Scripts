#!/usr/bin/python
#Decode VBA Macro based on chr() obfuscation
#Xavier Mertens <xavier@rootshell.be>
#
#
#Modified version, original is there :
#https://github.com/xme/toolbox/blob/master/deobfuscate_chr.py
#

# add reversestr parsing

import re 
import sys 

def reverseme(s):
  s= s.encode('string_escape')
  if s[len(s)-1] != ')':
    return s[::-1]
  return s[len(s)-2::-1]+')'
  

def do_chr (m):
  if m.group (0) :
    return eval(re.sub(r'[cC][hH][rR][wW\$]*\(([\d\+\-\s.]*)\)',r'chr(int(\1))', m.group(0))) 
  return "" 

def do_strme (m):
  if m.group (0) :
    return eval(re.sub(r'[sS][tT][rR][rR][eE][vV][eE][rR][sS][eE]\((.*)\)',r'reverseme("\1")', m.group(0))) 
  return "" 

f = open (sys.argv[1], 'rb') 
for line in f.readlines():
     line = re.sub (r'[cC][hH][rR][wW\$]*\(([\d+\+\-\s\.]*)\)', do_chr, line)
     line = re.sub (" & ", "", line) 
     line = re.sub ("& ", "", line)
     line = re.sub (r'[sS][tT][rR][rR][eE][vV][eE][rR][sS][eE]\((.*)\)', do_strme, line)
     line = line.rstrip ()
     print line
f.close () 
exit
