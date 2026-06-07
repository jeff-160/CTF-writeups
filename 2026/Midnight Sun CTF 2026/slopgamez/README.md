## slopegamez  

<img src="images/chall.png" width=600>

Immediately upon visiting the challenge webpage, we will notice that we are redirected to `/index.php?theme=themes/dark`.  

This suggests that `index.php` is fetching theme config files from the `/theme` directory, which hints at an LFI vulnerability.  

<img src="images/webpage.png" width=800>

We can use `php://filter` to leak the `index.php` source as Base64.  

<img src="images/lfi.png" width=800>

Base64-decoding the leaked contents reveals the flag in a comment.  

<img src="images/flag.png" width=800>

Flag: `midnight{w4ch00_t4lk1ng_4b0ut_w1ll1s}`