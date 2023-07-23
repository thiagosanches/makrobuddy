#!/bin/bash

rm -rf fat12.img && mkdir -p fat12/
truncate fat12.img -s 1M
mkfs.vfat -F12 -S512 fat12.img
mkdir -p img/
sudo mount -o loop fat12.img fat12/
sudo cp -ra ../lib/ ../sprites/ ../main.py fat12/
sudo umount fat12/
du -ha fat12.img
md5sum fat12.img
sudo cp fat12.img img/