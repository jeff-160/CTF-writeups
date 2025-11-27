## notepad

<img src="images/chall.png" width=600>

This challenge has the same setup as part 3. Our input is run against a flag checking WASM script, but the decryption logic is more complicated this time.  

<img src="images/wasm.png" width=500>

We can still reproduce the decryption logic using the hardcoded ciphertext in the WASM code to retrieve the flag.  

<img src="images/flag.png" width=600>

Flag: `picoCTF{6cdceedc31e02d455b03fff6f3b1288}`