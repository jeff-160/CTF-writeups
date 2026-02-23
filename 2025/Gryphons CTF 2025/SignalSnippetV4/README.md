## SignalSnippetV4

Category: Forensics  
Difficulty: Easy

<img src="images/chall.png" width=400>

We are provided with a `.wav` file that plays morse code.  

Running `exiftool` on the file reveals hex values in the metadata.  

<img src="images/metadata.png" width=600>

Decrypting each section and combining everything gives us the flag.  

Flag: `GCTF25{S1Gn4L_An4LysT}`