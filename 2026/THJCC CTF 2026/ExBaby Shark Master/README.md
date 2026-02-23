## ExBaby Shark Master  

<img src="images/chall.png" width=600>

We are given a packet capture to analyse.  

We can filter for the flag prefix in Wireshark using  `frame contains "THJCC"`, which will actually narrow it down to two packets.  

<img src="images/search.png" width=600>

Following the TCP stream will then reveal the flag.  

<img src="images/flag.png" width=600>

Flag: `THJCC{1t'S-3Asy*-r1gh7?????}`