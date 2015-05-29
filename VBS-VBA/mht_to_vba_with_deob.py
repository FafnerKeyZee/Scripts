#!/usr/bin/env python
# Fafner [_KeyZee_] :
# This code is using an important part of Didier Stevens
# Conversion from ole to vba is from him, I did few modifications for my needs
"""

Source code put in public domain by Didier Stevens, no Copyright
https://DidierStevens.com
Use at your own risk

# http://www.wordarticles.com/Articles/Formats/StreamCompression.php

History:
  2014/08/21: start
  2014/08/22: added ZIP support
  2014/08/23: added stdin support
  2014/08/25: added options extract and info
  2014/08/26: bugfix pipe

Todo:
"""

import OleFileIO_PL
import sys
import math
import os
import zipfile
import cStringIO
import zlib
import base64
import re

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
    return eval(re.sub(r'[sS][tT][rR][rR][eE][vV][eE][rR][sS][eE]*\(([^)]*)\)',r'reverseme("\1")', m.group(0)))
  return "" 

#Fix for http://bugs.python.org/issue11395
def StdoutWriteChunked(data):
    while data != '':
        sys.stdout.write(data[0:10000])
        try:
            sys.stdout.flush()
        except IOError:
            return
        data = data[10000:]

def ParseTokenSequence(data):
    flags = ord(data[0])
    data = data[1:]
    result = []
    for mask in [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80]:
        if len(data) > 0:
            if flags & mask:
                result.append(data[0:2])
                data = data[2:]
            else:
                result.append(data[0])
                data = data[1:]
    return result, data

def OffsetBits(data):
    numberOfBits = int(math.ceil(math.log(len(data), 2)))
    if numberOfBits < 4:
        numberOfBits = 4
    elif numberOfBits > 12:
        numberOfBits = 12
    return numberOfBits

def DecompressChunk(compressedChunk):
    header = ord(compressedChunk[0]) + ord(compressedChunk[1]) * 0x100
    size = (header & 0x0FFF) + 3
    flagCompressed = header & 0x8000
    data = compressedChunk[2:2 + size - 2]

    if flagCompressed == 0:
        return data, compressedChunk[size:]

    decompressedChunk = ''
    while len(data) != 0:
        tokens, data = ParseTokenSequence(data)
        for token in tokens:
            if len(token) == 1:
                decompressedChunk += token
            else:
                numberOfOffsetBits = OffsetBits(decompressedChunk)
                copyToken = ord(token[0]) + ord(token[1]) * 0x100
                offset = 1 + (copyToken >> (16 - numberOfOffsetBits))
                length = 3 + (((copyToken << numberOfOffsetBits) & 0xFFFF) >> numberOfOffsetBits)
                copy = decompressedChunk[-offset:]
                copy = copy[0:length]
                lengthCopy = len(copy)
                while length > lengthCopy: #a#
                    if length - lengthCopy >= lengthCopy:
                        copy += copy[0:lengthCopy]
                        length -= lengthCopy
                    else:
                        copy += copy[0:length - lengthCopy]
                        length -= length - lengthCopy
                decompressedChunk += copy
    return decompressedChunk, compressedChunk[size:]

def Decompress(compressedData):
    if compressedData[0] != chr(1):
        return None
    remainder = compressedData[1:]
    decompressed = ''
    while len(remainder) != 0:
        decompressedChunk, remainder = DecompressChunk(remainder)
        decompressed += decompressedChunk
    return decompressed

def SearchAndDecompress(data):
    position = data.find('\x00Attribut')
    if position == -1:
        compressedData = data
    else:
        compressedData = data[position - 3:]
    result = Decompress(compressedData)
    if result == None:
        return 'Error: unable to decompress'
    else:
        return result


def OLEDump(filename):
    if OleFileIO_PL.isOleFile(filename) is not True:
          print >>sys.stderr, 'Error - %s is not a valid OLE file.' % infile
          sys.exit(1)
    ole = OleFileIO_PL.OleFileIO(filename)

    
    for fname in ole.listdir():
            stream = ole.openstream(fname).read()
            if '\x00Attribut' in stream:
                line = SearchAndDecompress(stream)
 		line = re.sub (r'[cC][hH][rR][wW\$]*\(([\d+\+\-\s\.]*)\)', do_chr, line)
		line = re.sub (" & ", "", line)
		line = re.sub ("& ", "", line)
		line = line.replace("\"","")
		line = re.sub (r'[sS][tT][rR][rR][eE][vV][eE][rR][sS][eE]\(([^)]*)\)', do_strme, line)
		line = line.rstrip ()        
                StdoutWriteChunked(line)
    ole.close()
    return 

if len(sys.argv) > 1:
    f = file(sys.argv[1],"rb")
    data = f.read()
    f.close()
    found = re.search("^Content-Type: application/x-mso\r\n\r\n^((?:[A-Za-z0-9+/\r\n]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?)\r\n",data,re.DOTALL|re.MULTILINE|re.IGNORECASE)
    if found:
        stream = base64.b64decode(found.group(1))
	found2 = re.search('\x78\x9c',stream,re.MULTILINE)
	if found2:
		OLEDump(zlib.decompress(stream[found2.start():len(stream)]))
	else :
		print "No compression found !"
    else:
	print "Not Content-Type: application/x-mso !"
