## Pantone

Category: Forens
Difficulty: Easy

<img src="images/chall.png" width=400>

We are given a folder of images and a `.txt` file containing a list of passphrases. The challenge name heavily hints towards image steganography.  

We can write a simple script to bruteforce every passphrase against each image until the correct passphrase is found, then save the extracted text.  

The script is able to extract the data from all the files except for `smileandwave.jpeg`

<img src="images/extract.png" width=400>

Inside `business_is_flying_off_da_shelves.txt`, we find the first part of the flag, as well as another hint.  

<img src="images/first.png" width=600>

Trying an empty passphrase on `smileandwave.jpeg` then successfully extracts the text.  

<img src="images/smileandwave.png" width=500>

We find the second part of the flag and are able to assemble the full flag.  

<img src="images/second.png" width=500>

Flag: `GCTF25{a_hAp_pyFamiLy}`