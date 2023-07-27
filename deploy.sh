#!/bin/bash

rsync -avh lib/helpers/ "/media/$USER/CIRCUITPY/lib/helpers" 
rsync -avh sprites/ "/media/$USER/CIRCUITPY/sprites"
rsync -avh main.py "/media/$USER/CIRCUITPY"
