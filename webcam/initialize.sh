#!/bin/bash

# install v4l-utils
sudo yum install  v4l-utils

# check information of web camera
# dev name = XXX / ex) v4l/by-id/usb-0c45_USB_camera-video-index0
v4l2-ctl -d /dev/XXX --all

# check resolution of web camera
v4l2-ctl -d /dev/XXX --list-formats-ext

# set web camera with a specific resolution
v4l2-ctl -d /dev/XXX --set-fmt-video=width=<width>,height=<height> --set-parm=<refresh-rate>

cd software
. install-fswebcam.sh

