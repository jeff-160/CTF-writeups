## TypeFinder!

Category: Web  
Difficulty: Medium  

<img src="images/chall.png" width=400>

ragebait chall  

We are given a webpage with some additional functionalities.  

<img src="images/webpage.png" width=400>

In the `forgor.php` page, we can confirm that an admin account does indeed exist on the server.  

<img src="images/forgor.png" width=500>

We also have a file viewer page, which hints that there is a list of accounts on the server, but there's no instructions on how to use it. However, judging from the fact that `forgor.php` uses `q` for arguments, a reasonable guess would be that `view.php` uses `f` for file arguments.  

<img src="images/view.png" width=600>

That indeed works, and we are able to view the source code of `view.php`. From this, we learn that there is a whitelist of readable files, and `users.json` is indeed among them.  

<img src="images/view_php.png" width=500>

Viewing the source code for `login.php` also reveals the exact location of `users.json`.  

<img src="images/login_php.png" width=400>

Since `users.json` and the `.php` files are in different directories, we have to use path traversal to access it.  

```
http://chal1.gryphons.sg:8004/view.php?f=../../private/users.json
```

<img src="images/users.png" width=500>

Recalling the source code for `login.php`, the login page actually checks the MD5 hash of our entered password against the password stored on the server, so we can't just login with `0e462097431906509019562988736854` directly.  

However, we can simply get the preimage of the MD5 hash using [md5decrypt](https://md5decrypt.net/).  

<img src="images/md5decrypt.png" width=600>

Logging in with `admin` and `240610708` does indeed output the flag.  

<img src="images/flag.png" width=400>

Flag: `GCTF25{TypE_jugg13_th3$E_nuT$}`