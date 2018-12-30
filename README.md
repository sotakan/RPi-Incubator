# RPi-Incubator
## Use these schematics at your own risk!

### Features:  
Temperature Control  
Humidity Display  
Code is now legible  
Automatically select I2C address for LCD

### Todo:
Data logging  
OTA updates

### Setting up:
1. If you haven't, install git with `sudo apt-get update && sudo apt-get install -y git`  
2. Clone this repo with `git clone https://github.com/sotakan/RPi-Incubator.git`
3. Go to your newly cloned folder with `cd RPi-Incubator`
4. Make the installer executable with `sudo chmod a+x installer.sh`
5. Execute `./installer.sh` to install dependencies, enable I2C, make `exex.sh` executable, and change the hostname to `Incubator-Pi`.
6. Run `sudo python incubator.py` or `./exec.sh`(looped `sudo python incubator.py` to recover from random errors)  
*Extra tip: You may add the script to your [crontab](https://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/) to execute on @reboot.*

### Troubleshooting



Donations are appreciated!
https://www.amazon.jp/gp/registry/wishlist/2O0N3CM3FQTD    
Bitcoin: 1SoTAQrztSMsR51YhNKz5Vqordr2cHCHA   
Ether: 0xc28a9d2824fc329804700c23cd9602f3af9c67cf
