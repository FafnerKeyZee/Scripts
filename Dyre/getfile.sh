#!/bin/bash
payload=(`cat db3.txt`)

for ip in `cat db2.txt`
do
  valid=`curl -o /dev/null --silent --head --write-out '%{http_code}' $ip`
  if [ "$valid" != "000" ]
  then
    for pay in "${payload[@]}"
    do
      curl -o /dev/null --silent --head --write-out '%{http_code} %{url_effective}  \n' $ip/$pay --connect-timeout 10
    done
  fi
done
