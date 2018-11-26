#!/usr/bin/env bash
# Mount the two external harddrives used on the aurora
#
# Note that the configuration file used *must* be specified using the AIRBOX_CONFIG environment variable.
# This command can be run using the following command
# AIRBOX_CONFIG=~/airbox/config/airbox_config_v1.json ./scripts/unmount_drives.sh

# NOTE: The python executable and directory to the source code used is hardcoded

echo "Using configuration file: $AIRBOX_CONFIG"

echo "Mounting drives"
sudo mount /media/aurora_ext_aad
sudo mount /media/aurora_ext_uom

echo "Installing scheduler"
airbox install | sudo tee /etc/cron.d/airbox
sudo +x /etc/cron.d/airbox

echo "The airbox scheduler has been reenabled."