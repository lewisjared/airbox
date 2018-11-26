#!/usr/bin/env bash

# Backup the spectra data from MAXDOAS
# There are 1000s of very small files produced every day which slows down the backup process
# Instead of copying the files directly, a gzip archive will be stored. This is faster to generate

ROOT_DIR=/mnt/airbox/maxdoas/Data/v1_Oct2018

function mod_time() {
    ls -l -d --full-time $1 | cut -d " " -f 6,7
}

for m_dir in $ROOT_DIR/SP*/*; do
    for d_dir in $m_dir/SP??????; do
        if [ -f $d_dir.tar.gz ]; then
            # Check modified times
            dir_modtime=`mod_time $d_dir`
            f_modtime=`mod_time $d_dir.tar.gz`
            echo $dir_modtime $f_modtime
            if [[ $dir_modtime > $f_modtime ]]; then
                echo "Newer files exist. Creating archive $d_dir.tar.gz"
                tar -C $m_dir -zcf $d_dir.tar.gz $d_dir
            fi
        else
            echo "Creating archive $d_dir.tar.gz"
            tar -C $m_dir -zcf $d_dir.tar.gz $d_dir
        fi
    done
done