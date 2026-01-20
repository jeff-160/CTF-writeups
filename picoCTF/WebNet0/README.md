## WebNet0  

<img src="images/chall.png" width=600>

We are provided with a private RSA key and a packet capture.  

In Wireshark, we can find some packets that show a client key exchange.  

<img src="images/packets.png" width=600>

We can import the private key file into Wireshark protocol preferences, then follow the TLS stream of the packet. The TLS stream will be decoded, displaying the flag in the request headers.  

<img src="images/flag.png" width=600>

Flag: `picoCTF{nongshim.shrimp.crackers}`