#!/bin/bash

set -ex

prefix=""

if [ $# -eq 0 ]; then
    echo 'Please enter walltime'
    exit 1
fi

if [ $2 = "tampi" ]; then
    ./build.sh tampi
    prefix="tampi_"
else
    ./build.sh
fi

timestamp=$(date +%Y-%m-%d_%H-%M-%S)

job="submit.pbs"
jobID_full=$(qsub -l walltime=$1 $job)
jobID=$(echo "$jobID_full" | sed -e 's|\([0-9]*\).*|\1|')

numDone=0

while [ $numDone -lt 1 ]; do
    if [[ $(qstat $jobID) ]]; then
        sleep 60
    else
        mkdir yamls/"$timestamp"
        mv *.yaml yamls/"$timestamp"

        python output_parser.py CoMD.o"$jobID" timing_"$timestamp".dat
        mv timing_"$timestamp".dat results/"$prefix""$timestamp".dat
        mv CoMD.o"$jobID" results/"$prefix"CoMD_"$timestamp".dat
        numDone=1
    fi
done
