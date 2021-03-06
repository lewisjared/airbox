Changelog
=========

master
------

v1.0.2
------

- Create destination directories if they don't exist
- Add MIT license
- Fixed an off by one error when calculating the number of modified files
- Added sphinx docs
- Added configuration for v3 and v4
- Minor fixes before v2

v1.0.1
------

- Updated documentation
- Changed v2 configuration to reflect path changes

v1.0.0
------

- Removed verbose flags from backup_maxdoas.sh script
- Minor changes to logging
- install command now runs script in verbose mode for better debugging once I leave the ship
- Append current log to expeditioner email
- Added more commands to run on unmount

0.2.4
-----
- Additional filters on synced backups

0.2.3
-----

- Default logs to a /var/log/airbox folder
- Added script for tar'ing MAXDOAS spectra
- Sync between drives for `backup_sync`

0.2.2
-----

- Don't add additional quote marks to rsync commands

0.2.1
-----

- Disabled of sending emails to group members outside of the ship due to emails ending up in spam

0.2.0
-----

- Shifting mountpoints to /etc/fstab rather than trying to mount them during the backups
- Added `create_mounts` and `print_fstab` for managing the mounting of folders
- Addded more documentation
- Moved to a cron file in /etc/cron.d instead of /etc/cron.hourly
- Redirect the output from `airbox install` to /etc/cron.d instead of using python

0.1.3
-----

- Read in daily Spectronus data and added to plots
- Added subset command for extracting a data for a single instrument
- Remove nan values from met data
- Added backup sync command for syncronising the backups with the external drives which are removed from the vessel after the voyage
- Added scripts for removing and reenabling the external harddrives on the aurora

0.1.2
-----

- Added changelog
- Attachments are now fixed width in emails
- Added `args` parameter to a scheduler

0.1.0
-----

- Initial release of the project
- Airbox cli tool for running commands
- backup command for copying instruments using a customisable JSON configuration
- basic_plot for creating and sending simple plots to a list of users