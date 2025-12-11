#!/bin/bash
/usr/bin/flock -x --timeout 10 /home/dosue/software/dosue-daq/webcam/cronwebcam.lock -c ". /home/dosue/venv/env1/bin/activate; /home/dosue/software/dosue-daq/webcam/webcam_getpicture.py -u 0 " 2>&1> /home/dosue/software/dosue-daq/webcam/webcam_log.out
