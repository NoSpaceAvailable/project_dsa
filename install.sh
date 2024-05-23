#!/bin/bash
echo "[o] Your username: $(uname -n)"
sleep 1
echo "[o] Operating system: $(uname -o)"
sleep 1
echo "[o] Machine: $(uname -m)"
sleep 1
echo "[o] Kernel version: $(uname -v)"
sleep 1
echo "[o] Current directory: $(pwd)"
sleep 1
echo "[o] Checking dependencies ..."
sleep 2
python3 dependencies.py

python3 main.py