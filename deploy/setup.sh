#!/bin/bash
set -xe
cd /opt/ioiprint
chmod +x ./deploy/*.sh
if [ ! -e /opt/ioiprint_venv/.built-on-codebuild  ];then
  ./deploy/install-deps.sh
fi
