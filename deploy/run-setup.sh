#!/bin/bash
chmod +x /opt/ioiprint/deploy/setup.sh
exec sudo /usr/bin/systemd-run -P -p User=deploy -p MemoryMax= /opt/ioiprint/deploy/setup.sh
