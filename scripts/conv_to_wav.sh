#!/bin/sh

# dependencies: a working ffmpeg installation
# for instructions to install ffmpeg see: https://ffmpeg.org/download.html

# this script converts all the .mp3 files in the directory DIRPATH to the .wav file format

# DIRPATH
#   - DIRPATH is the path to the directory containing the .mp3 files
DIRPATH=$1

if [ -z "$DIRPATH" ]; then
    echo "Usage: $0 <DIRPATH>"
    exit 1
fi

OUTDIR=$DIRPATH/wav

# make the output directory if it doesn't exist
if [ ! -d "$OUTDIR" ]; then
    mkdir $OUTDIR
fi

# convert all .mp3 files in the directory to .wav files
for file in $DIRPATH/*.mp3; do
    filename=$(basename "$file")
    filename="${filename%.*}"
    ffmpeg -i $file $OUTDIR/$filename.wav
done

echo "Done!"