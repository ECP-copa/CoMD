#!/bin/bash

cd ../src-openmp
make clean
if [ $1 = "tampi" ]; then
    make tampi
else
    make
fi
