#!/bin/bash
#
# Work for "Microsoft Word 2007+" files
#
#Error code
# 0 - No Error \o/
# 1 - No MZ Bytes Inside :-(

myfile=$1
mycontent=
echo "Starting analysis of : "$myfile
mycontent=`unzip -p $myfile word/document.xml | sed -e 's/<[^>]\{1,\}>//g; s/[^[:print:]]\{1,\}//g'`
mycontent=`echo $mycontent | sed -e 's/ //g'`
data=`echo $mycontent | grep "4D5A9000030000000"`
if [ -z "$data" ]
then
  exit 1
fi
data=`echo $data | sed -e 's/.*4D5A9000030000000/4D5A9000030000000/'`
echo $data |xxd -r -p > $myfile.bin
#filetype=`file $myfile.bin`
#echo $filetype
exit 0
