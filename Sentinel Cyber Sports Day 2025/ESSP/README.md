<img src="images/challenge.png" width=400>

Inspecting the pcap file, we can see that requests are being sent over to the server on port 1337.  

<img src="images/port.png" width=600>

The user then sends a `START` command over to the server.  

<img src="images/start.png" width=600>

The server then gives the user the `LOGIN` prompt, where the user can enter a username to retrieve the playlist.  

<img src="images/login.png" width=600>
<img src="images/username.png" width=600>

We can automate this process over pwntools and enter the username `john` instead to get the flag.  

<img src="images/flag.png" width=600>