#!/bin/sh
sudo apt-get update
sudo apt-get install build-essential python-dev python-pip libffi-dev libgmp3-dev libmpfr-dev libmpc-dev -y
pip install -r requirements.txt
