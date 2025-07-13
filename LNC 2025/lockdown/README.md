## lockdown

Category: Misc  
Difficulty: Medium

<img src="images/challenge.jpeg" width=400>

We are given a Pyjail where the goal is to retrieve the `FLAG` variable.  

However, we notice that practically all ASCII characters are blacklisted.  

<img src="images/blacklist.png" width=600>

Clearly, this points towards a unicode bypass pyjail.  

We can put our payload through an [italic font generator](https://lingojam.com/ItalicTextGenerator) to easily bypass the blacklist.  

<img src="images/solve.jpeg" width=600>