## Gryphons Site

Category: Web  
Difficulty: Medium

<img src="images/chall.png" width=400>

We are given a webpage containing information about the Gryphons team members.  

<img src="images/webpage.png" width=600>

There is also an admin login page, but all attempts at SQLi fail, so the login can't be that straightforward.  

<img src="images/admin.png" width=400>

Going back to the team page, I found out that member information is fetched using `/members?id=1`.  

<img src="images/query.png" width=500>

Looking at the HTML source of one of the member pages, I found a suspiciously empty div.  

<img src="images/div.png" width=400>

I also found out that it is possible to leak errors when tampering with the `id` paramter in `/members`. Below was the message I got when I set it to `0`.  

<img src="images/leak.png" width=600>

Replacing `id` with an SQLi payload like `'--` gave a different error, which proved that the endpoint was vulnerable to SQLi.  

<img src="images/db.png" width=600>

Since this is essentially a blind SQLi, the most logical thing to do would be to leak the database structure and table information.  

Through trial and error, I was able to produce a working payload that leaked the structure of the first table in the database.  

```sql
0 union select sql,null,null,null,null,null from sqlite_master where type="table"
```

I wrote a Python script to bruteforce all possible tables by incrementing the `OFFSET` in the union attack.  

One of the tables leaked was `creds`, which could potentially contain all login credentials.  

<img src="images/creds.png" width=500>

By tweaking the payload a bit, I was able to leak all the accounts from `creds`.  

<img src="images/accounts.png" width=500>

My teammate was able to crack weiyan's password hash using `hashcat`, revealing that her password was `maple`.

Using the credentials, I was finally able to login to the admin dashboard.  

<img src="images/dashboard.png" width=600>

The flag wasn't in any of the pages on the dashboard, but I did manage to find a potential LFI vulnerability.  

<img src="images/lfi.png" width=600>

After some guesses, I found a file called `flag.html`, which displayed the Base64-encoded flag.  

<img src="images/flag.png" width=600>

Flag: `GCTF25{welcome_to_gryphons}`
