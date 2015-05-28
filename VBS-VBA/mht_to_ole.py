#!/usr/bin/python
#
# Use this script to extract ole part from a mht file
# Fafner [_KeyZee_]

import zlib
import base64
import re
import sys

if len(sys.argv) > 1:
    f = file(sys.argv[1],"rb")
    data = f.read()
    f.close()
    found = re.search("^Content-Type: application/x-mso\r\n\r\n^((?:[A-Za-z0-9+/\r\n]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)\r\n",data,re.DOTALL|re.MULTILINE|re.IGNORECASE)
    if found:
        stream = base64.b64decode(found.group(1))
	found2 = re.search('\x78\x9c',stream,re.MULTILINE)
	if found2:
		stream2 = zlib.decompress(stream[found2.start():len(stream)])
		f = file(sys.argv[1]+".ole","wb")
                f.write(stream2)
		f.close()
		print "Done !"
	else :
		print "No compression found !"
    else:
	print "Not Content-Type: application/x-mso !"
