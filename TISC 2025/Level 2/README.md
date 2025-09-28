<img src="images/challenge.png" width=600>

We are given a website where it appears we can send commands over to a bot for execution.  

Sending some random input gives this response.  

<img src="images/key.png" width=600>

Looking through the website source code, we find this comment.  

<img src="images/password.png" width=600>

The password is actually a vigenere cipher, and the bot's response seems to contain the key needed to decode it.  

Running them through an [online decoder](https://cryptii.com/pipes/vigenere-cipher) does indeed reveal the plaintext.  

<img src="images/cipher.png" width=600>

After prepending subsequent inputs with the keyword, the bot reveals an endpoint to us.  

<img src="images/endpoint.png" width=600>

However, if we prepend our endpoint with `/api`, it appears that the bot cannot locate the page.  

<img src="images/not found.png" width=600>

It appears that `/supersecretendpoint` is in the root directory instead. We can simply use path traversal to go down one directory and finally access the endpoint, giving us the flag.  

<img src="images/flag.png" width=600>