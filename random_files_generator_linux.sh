#!/bin/bash

head -c 1048576 /dev/urandom > files/1MB
head -c 104857600 /dev/urandom > files/100MB
head -c 1073741824 /dev/urandom > files/1GB