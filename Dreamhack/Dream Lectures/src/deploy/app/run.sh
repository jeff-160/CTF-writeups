#!/bin/bash

export MYSQL_USER=dbuser
export MYSQL_PASSWORD=dbpass

/usr/bin/mysqld_safe &
sleep 5
python3 app.py
