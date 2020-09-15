#!/bin/bash
#downloads the json config for the selected camera and saves it
wget http://127.0.0.1:$((1181 + $1))/config.json -O ~/.hawk/cameras/$1.json
