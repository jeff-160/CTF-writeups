## easyxss  

<img src="chall.png" width=600>

json injection --> arbitrary redirect --> xss with javascript:// redirect  

fetch /flag to leak httponly cookie --> exfil to webhook  

Flag: `pocas{010-2361-****}`