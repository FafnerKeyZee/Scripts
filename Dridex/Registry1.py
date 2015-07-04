#!/usr/bin/python

import re
import sys
import array

regedit = "Registry"

def key(m):
 if m.group (0) :
  lol = m.group(0)
  print lol
 return ""

with open(sys.argv[1], 'rb') as source_file:
  with open("tmp", 'w+b') as dest_file:
    contents = source_file.read()
    dest_file.write(contents.decode('utf-16').encode('utf-8'))
    dest_file.close()
  source_file.close()
f = open("tmp", 'r')
lines = f.readline()
total = lines.find(regedit,0,len(lines))
if (total < 0):
  print "Not a registry file"
  exit()
lines = f.readline()
lines = f.readline()

val = re.search(r'\{.*\}',lines)
if not val:
  print "Vide"
  exit()
val = val.group(0)
val = val.replace("{","")
val = val.replace("}","")
val = val.replace("-","")

content = f.read()
content = content.replace("\n","")
content = content.replace("\r","")
content = content.replace("\\","")
content = content.replace(" ","")
content = content.replace(",","")
content = content.split(':')[1]

key = bytearray( val.decode("hex"))
data = bytearray( content.decode("hex"))

l = len(key)
decoded = bytearray()
for i in range(0, len(data)):
        dec_byte = data[i] ^ key[i % l]
        decoded.append(dec_byte)
print decoded
