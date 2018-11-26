#!/usr/bin/env bash
# Unmount the two external harddrives used on the aurora
#
# This performs a final backup_sync to make sure the drives are in sync with the shared drive
# Note that the configuration file used *must* be specified using the AIRBOX_CONFIG environment variable.
# This command can be run using the following command
# AIRBOX_CONFIG=~/airbox/config/airbox_config_v1.json ./scripts/unmount_drives.sh

echo "Running final sync"
airbox backup_sync

echo "Unmounting drives"
sudo umount /media/aurora_ext_aad
sudo umount /media/aurora_ext_uom

echo "Uninstalling scheduler"
sudo rm /etc/cron.d/airbox

echo "Drives can now be removed. Replace with new drives and run 'aurora_remount_drives.sh' with the new configuration file"
echo "The airbox scheduler has been disabled until 'aurora_remount_drives.sh' has been called."