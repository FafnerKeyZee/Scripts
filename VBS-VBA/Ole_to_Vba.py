#!/usr/bin/env python
# Fafner [_KeyZee_] : Modified version for print only Macro
__description__ = 'Process command'
__author__ = 'Didier Stevens'
__version__ = '0.0.1'
__date__ = '2014/08/26'

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

import optparse
import OleFileIO_PL
import sys
import math
import os
import zipfile
import cStringIO


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
                StdoutWriteChunked(SearchAndDecompress(stream))
    ole.close()
    return 

def Main():
    oParser = optparse.OptionParser(usage='usage: %prog file\n' + __description__, version='%prog ' + __version__)
    (options, args) = oParser.parse_args()
    if len(args) != 1:
        oParser.print_help()
        print('')
        print('  Source code put in the public domain by Didier Stevens, no Copyright')
        print('  Use at your own risk')
        print('  https://DidierStevens.com')
	print
        print('  Modified Version By Fafner [_KeyZee_]')
	print('  Only print Macro nothing else')
        return
    elif len(args) == 0:
        OLEDump('')
    else:
        OLEDump(args[0])

if __name__ == '__main__':
    Main()
