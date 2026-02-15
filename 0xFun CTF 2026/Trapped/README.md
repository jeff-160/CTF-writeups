## Trapped  

<img src="images/chall.png" width=600>

In the challenge server, we are provided with `flag.txt`, but we don't have permission to read it.  

<img src="images/denied.png" width=600>

Running `getfacl` on the flag file will show that it is root owned, and will also reveal that `secretuser` has root privileges.  

<img src="images/perms.png" width=600>

We can find the password for `secretuser` in `/etc/passwd`.  

<img src="images/password.png" width=600>

We can then `su` with the `secretuser` password to get a shell with root privileges, where we can read the flag file.  

<img src="images/flag.png" width=600>

Flag: `0xfun{4ccess_unc0ntroll3d}`