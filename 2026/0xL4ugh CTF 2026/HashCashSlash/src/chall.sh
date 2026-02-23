# !/bin/bash

# NOTE: THIS WAS NOT PROVIDED IN THE CHALL DIST, THIS WAS FETCHED FROM THE SHELL

read -e -r x
[[ "$x" =~ ^[\\#\$]+$ ]] || exit 1
printf -v cmd '%s ' bash -c "\"${x}\""