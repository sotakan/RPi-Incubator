#!/bin/bash

#Installs software
echo "Installing dependencies"
sudo apt-get update && sudo apt-get install -y git i2c-tools python-smbus mysql.connector python-pycurl | echo "Download Success!"
echo "Cloning git repository"
git clone https://github.com/sotakan/RPi-Incubator.git

# Enable I2C
echo "Editing /boot/config.txt to enable I2C"
grep -q -F -w "\<dtparam=i2c_arm=on\>" /boot/config.txt || sudo sed -i "s/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/" /boot/config.txt
echo "Editing /etc/modules to enable I2C"
grep -q -F "i2c-dev" /etc/modules || printf "\ni2c-dev" | sudo tee -a /etc/modules

#Make exec.sh executable
sudo chmod a+x $PWD/exec.sh

#Change hostname
echo "Incubator-Pi" | sudo tee /etc/hostname
