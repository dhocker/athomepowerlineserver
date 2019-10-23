#!/bin/bash

### Uninstall (remove) AtHomePowerlineServerD.sh as a daemon

# Uninstall steps
sudo service AtHomePowerlineServerD.sh stop
sudo rm /etc/init.d/AtHomePowerlineServerD.sh
sudo update-rc.d -f AtHomePowerlineServerD.sh remove

exit 0

