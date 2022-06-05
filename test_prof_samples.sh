#!/bin/bash

set -xe

port=50124
ips=(v4 v6)
client_hostnames=(127.0.0.1 ::1)

client_entries='\
add sensor 01 03 in 02
add sensor 01 in 02
add sensor 02 in 02
list sensors in 02
add sensor 03 in 01
add sensor 01 in 01
list sensors in 01
read 01 04 in 01
kill
quit
'
expected_responses='\
sensor 01 03 added
sensor 01 already exists in 02
sensor 02 added
01 03 02
sensor 01 removed
sensor 01 does not exist in 02
03 02
sensor 03 added
sensor 01 added
03 01
sensor(s) 04 not installed
'

for i in 0 1; do
    ./server ${ips[$i]} $port -log-level=INFO
    echo -n "$client_entries" | ./client ${client_hostnames[$i]} $port -log-level=INFO > temp1.txt
    echo -n expected_responses > temp2.txt
    diff temp{1,2}.txt 2>&1 >/dev/null
    [ "$?" != "0" ] && echo Failure && exit 1
done

rm -f temp{1,2}.txt
