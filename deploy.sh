#!/bin/bash

mkdir -p "/media/$USER/CIRCUITPY/lib"
mkdir -p "/media/$USER/CIRCUITPY/sprites"
mkdir -p "/media/$USER/CIRCUITPY/fonts"

# 'minifing' a little bit the json config files.
find sprites/ -name '*.json' -exec cp {} {}.tmp \;
find sprites/ -name '*.tmp' -print0 | xargs -0 -I {} bash -c 'NEW_NAME=$(echo {} | sed 's/tmp/min/g'); cat {} | tr "\n" " " | sed "s/ //g" > $NEW_NAME'
find sprites/ -name '*.tmp' -exec rm -rf {} \;

rsync -avhru --delete "lib" "/media/$USER/CIRCUITPY"
rsync -avhru --ignore-existing "fonts" "/media/$USER/CIRCUITPY"
rsync -avhru --delete --exclude "*.json" "sprites" "/media/$USER/CIRCUITPY"
rsync -avhru --delete "main.py" "/media/$USER/CIRCUITPY"

# synchronize cached writes to persistent storage.
sync
