#!/usr/bin/env python

# Original code in vbs by Jean-Luc Antoine, this is a python Version
# Usage : ./getvbs.py file.vbe

'''
'===============================================================================
'===============================================================================
'  SCRIPT........:  scriptDecode.vbs	
'  VERSION.......:  1.5
'  DATE..........:  11/22/2003
'  AUTHOR........:  Jean-Luc Antoine
'  LINK..........:  http://www.interclasse.com/scripts/decovbe.php
'  ALTERED BY....:  Joe Glessner
'  DESCRIPTION...:  Decodes scripts encoded with screnc.exe. Usable with 
'                   Wscript by dragging an encoded script onto this one. If done
'                   this way, only the first 100 lines (or so) of the script 
'                   will be displayed.
'                   If run using Cscript.exe the entire output will be 
'                   displayed.
'                   This script can be used to output the decoded script to a 
'                   file using Cscript.exe by calling it with the following
'                   syntax:
'
'              cscript [Path]\scriptDecoder.vbs [Path]\<filename> >> output.txt 
'
'===============================================================================
'===============================================================================
'''

import os
import sys

if len(sys.argv) != 2 :
  exit()

myfile = open(sys.argv[1],'r')
content = myfile.read()
myfile.close()

encInit = "#@~^CQUAAA=="
encEnd = "==^#~@"

beg = content.find(encInit)
end = content.find(encEnd)

content = content[beg+12:end-6]
#print content

combinaison="1231232332321323132311233213233211323231311231321323112331123132"
tDecode=[""]*128

decfile = open("test.bin",'r')
for i in range(9,128) :
    tmp = decfile.readline()
    tmp=tmp.split(' ')
    for val in range(0,3):
        tDecode[i]+=chr(int(tmp[val],16))

content=content.replace("@&",chr(10)).replace("@#",chr(13))
content=content.replace("@*",">").replace("@!","<")
content=content.replace("@$","@")


index=-1
NewContent = ''
content=list(content)
for i in range(0,len(content)):
            c=ord(content[i])
            if c<128 :
                index=index+1
            if (c==9) or ((c>31) and (c<128)) : 
                if (c!=60) and (c!=62) and (c!=64) :
                    content[i] = tDecode[c][int(combinaison[index%64])-1]

	    
content=''.join(content)
print content
