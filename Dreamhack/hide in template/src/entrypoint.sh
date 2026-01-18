#!/bin/sh

export FLAG=$(cat /flag.txt)

sed -i "s/\[FLAG\]/$FLAG/g" /app/templates/flag.html

echo $FLAG

rm /flag.txt

python3 /app/app.py