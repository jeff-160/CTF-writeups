#!/bin/sh
/etc/init.d/xinetd restart

/bin/bash
socat TCP-LISTEN:3001,reuseaddr,fork EXEC:'su bisc -c /run.sh'
sleep infinity

