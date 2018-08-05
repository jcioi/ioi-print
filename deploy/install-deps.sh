#!/bin/bash
set -xe
python3 -m venv /opt/ioiprint_venv
source /opt/ioiprint_venv/bin/activate
pip install --no-cache-dir -r requirements.txt
