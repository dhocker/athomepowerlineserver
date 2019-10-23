#!/bin/bash

### Install AtHomePowerlineServerD.sh as a daemon

# Installation steps
sudo cp AtHomePowerlineServerD.sh /etc/init.d/AtHomePowerlineServerD.sh
sudo chmod +x /etc/init.d/AtHomePowerlineServerD.sh
sudo update-rc.d AtHomePowerlineServerD.sh defaults

# Start the daemon: 
sudo service AtHomePowerlineServerD.sh start

exit 0

