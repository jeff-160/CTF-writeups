<img src="images/challenge.png" width=600>

Upon accessing the webpage, it seems that we have to submit a valid JWT token to retrieve the flag.  

<img src="images/webpage.png" width=600>

The console messages gave us a hint on how to construct the token and even gave the secret key. How nice.

<img src="images/hint.png" width=600>

We are given a sample JWT token. Since the current JWT.io UI is trash, we can use the [Wayback Machine snapshot](https://web.archive.org/web/20250115225215/https://jwt.io/) instead.

<img src="images/sample.png" width=500>

On decoding, it appears that we have to fill in the fields with the correct arguments to get the correct payload.  

<img src="images/payload.png" width=600>

Going back to the webpage, we see that there are multiple cookies, with some corresponding to the JSON payload fields. 

<img src="images/cookies.png" width=500>

We can simply URL decode the cookie data and add them into our payload, then use the provided secret key to encode the payload, giving us the valid JWT token.  

<img src="images/token.png" width=600>

Submitting the token in the webage then gives us the flag.  

<img src="images/flag.png" width=600>