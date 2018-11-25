Changelog
=========

master
------

- Shifting mountpoints to /etc/fstab rather than trying to mount them during the backups
- Added `create_mounts` and `print_fstab` for managing the mounting of folders
- Addded more documentation
- Moved to a cron file in /etc/cron.d instead of /etc/cron.hourly
- Redirect the output from `airbox install` to /etc/cron.d instead of using python

0.1.2
-----

- Read in daily Spectronus data and added to plots
- Added subset command for extracting a data for a single instrument
- Remove nan values from met data
- Added backup sync command for syncronising the backups with the external drives which are removed from the vessel after the voyage
- Added scripts for removing and reenabling the external harddrives on the aurora

0.1.1
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