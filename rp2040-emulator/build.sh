#!/bin/bash

rm -rf fat12.img
mkdir -p fat12/
truncate fat12.img -s 1M
mkfs.vfat -F12 -S512 fat12.img
mkdir -p img/
sudo mount -o loop fat12.img fat12/
sudo cp -ra ../lib/ ../sprites/ ../code.py fat12/
sudo umount fat12/