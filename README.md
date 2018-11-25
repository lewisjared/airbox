# AirBox Backups

This repository contains helper commands for performing backups of the airbox instruments.

These commands are managed by the `airbox` command line tool.

## Dependencies

This project is developed for running on the AirBox server which uses Ubuntu 18.04 as an operating system. `airbox` may
work for other operating systems or servers, but it has not been tested with any others. The operations for performing
the backups is offloaded to `rsync`, a program specifically created for performing backups. The following dependencies
are required:

* rsync
* cifs-utils

## Getting Started

This project uses a conda environment to manage the python packages required to run the airbox script. This conda
environment requires bootstrapping before use.

```
conda env create -n airbox python=3.6
conda install
conda activate airbox
cd airbox
python setup.py develop
```

To run the `airbox` command line tool, `conda activate airbox` must be called to ensure the correct version of python is
used. A configuration file is required to run any of the commands using the airbox tool. These config files are typically
added to the repository in the `config/` directory. See `config/airbox_config_v1.json` for an example. The configuration
file to use is specified using the `--config` argument. Alternatively, the configuration filename can be specified using
the `AIRBOX_CONFIG` environment variable.

See `airbox -h` for a list of commands which can be run. To see more information about a command, including a list
 of possible arguments add -h after the command.

```bash
airbox backup -h
```

```bash
sudo /home/airbox/miniconda3/envs/airbox/bin/python airbox/cli.py --config config/airbox_config_v1.json install
```


## Updating configuration for a new voyage

```bash
export AURORA_CONFIG=~/airbox/config/airbox_config_v1.json
./scripts/aurora_unmount_drives.sh
sudo mv /var/log/airbox.log /var/log/airbox_v1.log

# REMOVE and replace the external harddrives

export AURORA_CONFIG=~/airbox/config/airbox_config_v2.json
./scripts/aurora_remount_drives.sh
```

Be careful with the v1 and v2's. v1 is the current voyage and v2 is the next voyage.

## Troubleshooting

If the mounts to a computer is not working try the following steps:
* Ensure the username, password and IP address are correct.
* In "Network and Sharing Center" > "Advanced sharing settings", ensure that "File and Printing sharing" is enabled.