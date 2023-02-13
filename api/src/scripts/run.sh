#!/usr/bin/env bash

# Start app
echo "========>  Start app  <========"
cron
python3 -m code.api || exit 14
echo "========>  Run script: Done  <========"
