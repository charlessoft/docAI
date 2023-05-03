#!/bin/bash
/usr/local/bin/killport 18883
nohup python3 -u gptengine/main.py &
