# AirBox Backups

This repository contains helper scripts for performing backups of the airbox instruments.

## Dependencies

This project is developed for running on the AirBox server which uses Ubuntu 18.04 as an operating system. `airbox` may
work for other operating systems or servers, but it has not been tested with any others. The operations for performing
the backups is offloaded to `rsync`, a program specifically created for performing backups. The following dependencies
are required:

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

## Updating configuration for a new voyage

```
ssh airbox@airbox
sudo /home/airbox/miniconda3/envs/airbox/bin/python airbox/cli.py --config config/airbox_config_v1.json install
```



## Troubleshooting

If the mounts to a computer is not working try the following steps:
* Ensure the username, password and IP address are correct.
* In "Network and Sharing Center" > "Advanced sharing settings", ensure that "File and Printing sharing" is enabled.