## Danger  

<img src="images/chall.png" width=600>

In the challenge server, we are provided with a singular file `flag.txt`, but we don't have the perms to read it.  

<img src="images/denied.png" width=600>

Looking at the file privileges, we can see that only user `noaccess` has read access to `flag.txt`, but we are currently logged in as `Danger`.  

<img src="images/perms.png" width=600>

We can use `find` to list all the binaries that are owned by `noaccess`, and the one that is of most interest to use would be `/usr/bin/xxd`.  

`/usr/bin/xxd` runs as `noaccess`, and has the group permission `r-x`, which means any user can run it.  

<img src="images/xxd.png" width=600>

We can thus us `/usr/bin/xdd` to read the flag file.  

<img src="images/flag.png" width=600>

Flag: `0xfun{Easy_Access_Granted!}`