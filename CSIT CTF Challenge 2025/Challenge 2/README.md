<img src="images/challenge.png" width=600>

We are given a `.txt` file. Opening it in Notepad reveals a bunch of gibberish, so the next step would be to check the file type.  

<img src="images/file.png" width=600>

After renaming it with the `.zip` extension, we can then extract the zip archive, revealing two files.  
  
The second audio file appears to be Morse code, so we can simply run it through an [online decoder](https://morsecode.world/international/decoder/audio-decoder-adaptive.html).

<img src="images/part2.png" width=600>

The first audio file on the other hand, appears to be [DTMF](https://en.wikipedia.org/wiki/DTMF_signaling). It's basically the sounds on those old ahh telephones.  

Running it through an [online decoder](https://dtmf.netlify.app/) produces the following.  

<img src="images/dtmf.png" width=600>

At first glance, the above sequence appears to be gibberish, however, we can map the numbers to the DTMF keypad. We split the cipher by the `#`, then map the digits based on the key presses (2nd digit is the number of times the 1st digit is pressed).  

<img src="images/keypad.jpg" width=400>
  
Putting everything together, we get the flag: `CSIT{NSCITYH@LLS7AT10N}`