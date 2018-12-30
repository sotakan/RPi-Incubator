#!/bin/bash

# Installing dependencies
sudo apt-get update && sudo apt-get install -y mysql.connector python-pycurl
# Make new exec.sh executable
sudo chmod a+x $PWD/exec.sh

echo "Done!"
