==============
AirBox Backups
==============

This repository contains helper commands for performing backups of the airbox instruments.

These commands are managed by the `airbox` command line tool.

Dependencies
------------

This project is developed for running on the AirBox server which uses Ubuntu 18.04 as an operating system. `airbox` may
work for other operating systems or servers, but it has not been tested with any others. The operations for performing
the backups is offloaded to `rsync`, a program specifically created for performing backups. The following dependencies
are required:

* rsync
* cifs-utils

Getting Started
---------------

This project uses a conda environment to manage the python packages required to run the airbox script. This conda
environment requires bootstrapping before use.

.. code-block:: bash

    conda env create -n airbox python=3.6
    conda install
    conda activate airbox
    cd airbox
    python setup.py develop

To run the `airbox` command line tool, `conda activate airbox` must be called to ensure the correct version of python is
used. A configuration file is required to run any of the commands using the airbox tool. These config files are typically
added to the repository in the `config/` directory. See `config/airbox_config_v1.json` for an example. The configuration
file to use is specified using the `--config` argument. Alternatively, the configuration filename can be specified using
the `AIRBOX_CONFIG` environment variable. This can be set for the current terminal using `export AIRBOX_CONFIG=~/airbox/config/airbox_config_v1.json`

See `airbox -h` for a list of commands which can be run. To see more information about a command, including a list
 of possible arguments add -h after the command, e.g.: `airbox backup -h`

For a fresh install (or if any instruments are added or removed), a few steps are required to reconfigure the mount points
for the various computers which contain data. The configuration for mounting the remote directories from each of the 
instruments should be added to /etc/fstab. The command `print_fstab` prints the required lines to stdout (appending 
`2> /dev/null` to the command supresses the log messages which are written to stderr). The editing of /etc/fstab should 
be preformed manually, rather than redirecting the output to /etc/fstab just to be safe. The folder structure for the 
mount directories can be created using the command `create_mounts` before the `mount -a` command is run.

.. code-block:: bash

    $ airbox print_fstab 2> /dev/null
    //147.66.74.100/HgLoggerPlus    /mnt/airbox/tekran/HgLoggerPlus cifs    user=2537X,pass=,uid=1000,gid=1000,iocharset=utf8,noperm        0       0
    //147.66.74.97/Data     /mnt/airbox/maxdoas/Data        cifs    user=localadmin,pass=password,uid=1000,gid=1000,iocharset=utf8,noperm   0       0
    //147.66.74.102/nais    /mnt/airbox/nais/nais   cifs    user=NAIS,pass=nais21,uid=1000,gid=1000,iocharset=utf8,noperm   0       0
    //147.66.74.117/data    /mnt/airbox/minimpl/data        cifs    user=mpluser,pass=mpluser,uid=1000,gid=1000,iocharset=utf8,noperm       0       0
    //147.66.74.103/dmt     /mnt/airbox/ccn/dmt     cifs    user=aaeon,pass=password,uid=1000,gid=1000,iocharset=utf8,noperm        0       0
    //147.66.74.119/Data2   /mnt/airbox/acsm/Data2  cifs    user=user,pass=TofPass,uid=1000,gid=1000,iocharset=utf8,noperm  0       0
    //147.66.74.196/Data    /mnt/airbox/cims/Data   cifs    user=tofuser,pass=cimsuser,uid=1000,gid=1000,iocharset=utf8,noperm      0       0
    //147.66.74.101/AIRBOX  /mnt/airbox/ansto/AIRBOX        cifs    user=ANSTO,pass=password,uid=1000,gid=1000,iocharset=utf8,noperm        0       0
    //147.66.74.70/iPort    /mnt/airbox/ozone/iPort cifs    user=CAC,pass=gone-fishing,uid=1000,gid=1000,iocharset=utf8,noperm      0       0
    //147.66.74.104/Data    /mnt/airbox/csiro/Data  cifs    user=acc-field,pass=password,uid=1000,gid=1000,iocharset=utf8,noperm    0       0
    //147.66.74.101/UMB-Config      /mnt/airbox/ansto/UMB-Config    cifs    user=ANSTO,pass=password,uid=1000,gid=1000,iocharset=utf8,noperm        0       0
    //147.66.74.24/Data     /mnt/airbox/spectronus/Data     cifs    user=Ecotech,pass=airbox,uid=1000,gid=1000,iocharset=utf8,noperm        0       0
    $ sudo nano /etc/fstab
    $ sudo `airbox create_mounts`
    $ sudo mount -a

Finally, the scheduler can be installed to automatically run every hour using:

.. code-block:: bash

    airbox install | sudo tee /etc/cron.d/airbox
    sudo +x /etc/cron.d/airbox

If any errors occur during the execution of the backups the expeditioners will be emailed with the log output.

Updating configuration for a new voyage
---------------------------------------

.. code-block:: bash

    export AURORA_CONFIG=~/airbox/config/airbox_config_v1.json
    ./scripts/aurora_unmount_drives.sh
    sudo mv /var/log/airbox.log /var/log/airbox_v1.log

# REMOVE and replace the external harddrives

.. code-block:: bash

    export AURORA_CONFIG=~/airbox/config/airbox_config_v2.json
    ./scripts/aurora_remount_drives.sh

Be careful with the v1 and v2's. v1 is the current voyage and v2 is the next voyage.


Development setup
-----------------

Airbox isn't connected to the internet most of the time so deploying code can be difficult. In the case where the
airbox server can be accessed, rsync can be used to copy the code from your machine to the server
.. code-block:: bash

    rsync -avC --delete --exclude __pycache__ ~/code/airbox/airbox/ airbox:~/airbox

This assumes that the root directory for this repository is `~/code/airbox` on the local machine, the target destination
is `/home/airbox/airbox` and you have added the host airbox to your `~/.ssh/config` file, otherwise you need to specify 
the username (`airbox`) and ip address. On the Aurora Australis the IP address for the airbox server is `147.66.74.71`.

Troubleshooting
---------------

If the mounts to a computer is not working try the following steps:

* Ensure the username, password and IP address are correct. You should be able to login to remote desktop using these
credentials.
* In "Network and Sharing Center" > "Advanced sharing settings", ensure that "File and Printing sharing" is enabled.
