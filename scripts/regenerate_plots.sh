#!/usr/bin/env bash

START_DATE="2018-10-25"
END_DATE="2018-11-13" #  Exclusive of the end date
D=$START_DATE

export AIRBOX_CONFIG=config/airbox_config_v1.json

while [ $D != $END_DATE ]; do
    echo $D
    airbox basic_plot -d $D

    # Increment to the next day
    D=`date "+%Y-%m-%d" -u -d "$D + 1 day"`
done