#!/bin/bash

mkdir -p "/media/$USER/CIRCUITPY/lib"
mkdir -p "/media/$USER/CIRCUITPY/sprites"
mkdir -p "/media/$USER/CIRCUITPY/fonts"

rsync -avhru --delete "lib" "/media/$USER/CIRCUITPY"
rsync -avhru --delete "fonts" "/media/$USER/CIRCUITPY"
rsync -avhru --delete "sprites" "/media/$USER/CIRCUITPY"
rsync -avhru --delete "main.py" "/media/$USER/CIRCUITPY"

# synchronize cached writes to persistent storage.
sync
