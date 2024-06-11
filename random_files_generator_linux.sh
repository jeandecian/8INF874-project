#!/bin/bash

head -c 1048576 /dev/urandom > files/1MB

head -c 10485760 /dev/urandom > files/10MB
head -c 26214400 /dev/urandom > files/25MB
head -c 52428800 /dev/urandom > files/50MB
head -c 78643200 /dev/urandom > files/75MB

head -c 104857600 /dev/urandom > files/100MB
head -c 262144000 /dev/urandom > files/250MB
head -c 524288000 /dev/urandom > files/500MB
head -c 786432000 /dev/urandom > files/750MB

head -c 1073741824 /dev/urandom > files/1GB
head -c 2147483648 /dev/urandom > files/2GB
head -c 5368709120 /dev/urandom > files/5GB