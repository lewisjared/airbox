# AirBox Backups

This repository contains helper scripts for performing backups of the airbox instruments.

## Dependencies


* rsync
* cifs-utils


## Concepts

Within AirBox we have a number of instruments. Each instruments logs to a `Computer`


## Getting Started

Update settings in script to match your email address and config file

The script can then be copied into /etc/cron.hourly to be automatically run every hour. 

```
sudo copy airbox-backup.example /etc/cron.hourly/airbox-backup
sudo chmod +x /etc/cron.hourly/airbox-backup
```



## Troubleshooting

If the mounts to a computer is not working try the following steps:
* Ensure the username, password and IP address are correct.
* In "Network and Sharing Center" > "Advanced sharing settings", ensure that "File and Printing sharing" is enabled.