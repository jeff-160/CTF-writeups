## Travel Playlist  

<img src="images/chall.png" width=600>

We are given a webpage where we can fetch music videos from indexes `1-7`.  

<img src="images/webpage.png" width=600>

When we submit an input and intercept the request in BurpSuite, we will find that the webpage makes a request to `/api/get_json`.  

<img src="images/api.png" width=600>

Entering `1/../../../` will reveal that the server attempts to read files from `/static`.  

<img src="images/fetch.png" width=600>

We can use directory traversal to read `/etc/passwd`, confirming the LFI vuln.  

<img src="images/lfi.png" width=600>

The challenge description already reveals the file path is in `/app/flag.txt`, and since most challenge dockers add the source code in `/app`, we just have to traverse one directory up to read `flag.txt`.  

<img src="images/flag.png" width=600>

Flag: `pascalCTF{4ll_1_d0_1s_tr4v3ll1nG_4r0und_th3_w0rld}`