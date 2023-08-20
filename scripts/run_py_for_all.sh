#!/bin/sh

# a helper script in bash that loops through the all the files in 
# DIRPATH and runs the FILENAME script with each file as the argument

# DIRPATH
DIRPATH=$1

if [ -z "$DIRPATH" ]; then
    echo "Usage: $0 <DIRPATH>"
    exit 1
fi

FILENAME=remove_trailing_silence.py

# loop through all .wav files in the directory
for file in $DIRPATH/*.wav; do
    python ./$FILENAME -i $file
done