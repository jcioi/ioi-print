#!/usr/bin/env bash
cd /usr/src/ioiprint

if [[ $1 =~ /* ]]; then
    exec "$@"
fi

exec python3 run.py
