## [RV] Flag 2

<img src="images/chall.png" width=600>

Using `smbclient`, we can see that the provided credentials has access to an `Onboarding` share.  

<img src="images/shares.png" width=600>

In the share, we can find a `Interns2026.xlsx` file.  

<img src="images/dir.png" width=600>

This file actually contains the credentials of some interns.  

<img src="images/interns.png" width=600>

We can use one of the intern's credentials to connect to the Windows machine on `.20`.  

```bash 
evil-winrm -i 10.3.10.20 -u 'JEZZCORP\J.Kumar' -p Z7pLr2Qa
```

We can then `cd` into `/Users` to get flag 2.  

<img src="images/flag2.png" width=600>

Flag: `YBN25{1095744decaa363007c1d480b6d22759}`