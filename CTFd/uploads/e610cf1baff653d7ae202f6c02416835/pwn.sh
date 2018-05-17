#!/bin/sh
#name:pwn.sh
socat tcp-l:9999,fork exec:"python wrapper.py"
