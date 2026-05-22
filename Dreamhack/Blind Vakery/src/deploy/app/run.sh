#!/bin/sh

/usr/bin/mysqld_safe &
sleep 4
python3 app.py