#!/bin/bash

#Installs software
echo "Downloading..."
sudo apt-get update && sudo apt-get install -y git i2c-tools python-smbus
git clone https://github.com/sotakan/RPi-Incubator.git
git clone https://github.com/sotakan/i2clcd.git

echo "Copy and removing unnecessary files..."
cp i2clcd/i2clcd.py RPi-Incubator/i2clcd.py
rm -rf i2clcd

echo "Editing to enable I2C"
grep -q -F -w "\<dtparam=i2c_arm=on\>" /boot/config.txt || sudo sed -i "s/#dtparam=i2c_arm=on/dtparam=i2c_arm=on/" /boot/config.txt
grep -q -F "i2c-dev" /etc/modules || printf "\ni2c-dev" | sudo tee -a /etc/modules

#Creating exec.sh
touch exec.sh
printf "python RPi-Incubator/incubator.py" | sudo tee exec.sh

#Change hostname
echo "Incubator-Pi" | sudo tee /etc/hostname
