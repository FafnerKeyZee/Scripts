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

pos=0
while pos< len(decoded):
	tag=decoded[pos]
        print "Pos : %x => %d" % (pos,tag)
        if tag==7 :
		temp=pos
		pos=pos+4
	size=decoded[pos+4]
	size= decoded[pos+5]*256+size
	key = bytearray()
	key.append(decoded[pos+6])
	key.append(decoded[pos+7])
	key.append(decoded[pos+8])
	key.append(decoded[pos+9])
	next=pos+size+6
	data=bytearray(decoded[pos+10:next])

	l = len(key)
	conf = bytearray()
	for i in range(0, len(data)):
		dec_byte = data[i] ^ key[i % l]
		conf.append(dec_byte)
        print conf
        pos=next
        if tag ==6:
          click=decoded[next+1]*256+decoded[next]
          x=decoded[next+3]*256+decoded[next+2]
          y=decoded[next+5]*256+decoded[next+4]
          print "Click : %d => X : %d => Y : %d"% (click, x, y)
          pos=pos+6
        if tag ==7:
          pos=pos+53
          print "%x" %pos
	  size=decoded[pos+4]
	  size= decoded[pos+5]*256+size
	  key = bytearray()
  	  key.append(decoded[pos+6])
 	  key.append(decoded[pos+7])
 	  key.append(decoded[pos+8])
 	  key.append(decoded[pos+9])
 	  next=pos+size+6
	  data=bytearray(decoded[pos+10:next])

	  l = len(key)
	  conf = bytearray()
	  for i in range(0, len(data)):
		dec_byte = data[i] ^ key[i % l]
		conf.append(dec_byte)
          print conf
          pos=next
	  pos=pos+1+4
	  size=decoded[pos+4]
	  size= decoded[pos+5]*256+size
          print "size %x" % size

	  key = bytearray()
  	  key.append(decoded[pos+6])
 	  key.append(decoded[pos+7])
 	  key.append(decoded[pos+8])
 	  key.append(decoded[pos+9])
 	  next=pos+size+6
	  data=bytearray(decoded[pos+10:next])

	  l = len(key)
	  conf = bytearray()
	  for i in range(0, len(data)):
		dec_byte = data[i] ^ key[i % l]
		conf.append(dec_byte)
          print conf
          pos=next
          temp=next-temp
	  print "Jump : %d"% temp
          
	
