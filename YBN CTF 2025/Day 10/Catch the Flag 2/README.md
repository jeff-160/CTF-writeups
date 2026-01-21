## Catch the Flag 2  

<img src="images/chall.jpeg" width=600>

This challenge requires us to figure out and go to the admins' physical location to get the flag. We are provided with only an image to analyse.  

Opening the image in aperisolve, we can notice that some of the bit planes have a recurring pattern in the top left corner-a thin line of pixels.  

<img src="images/pattern.png" width=600>

In [StegOnline](https://georgeom.net/StegOnline/extract), we can select only the rows with the pattern and extract data from them. This will produce a Base64 string that decodes to `https://drive.google.com/file/d/1kyfxAskszcoZ19Qtgey-aSFDsYcK1U94/view?usp=sharing`.  

<img src="images/b64.png" width=600>

The drive link will lead us to a `.pcapng` file that we can open in Wireshark.  

One of the TCP packets appears to have ran shell commands on a vulnerable machine, which caused it to output a discord invite link, although redacted.  

<img src="images/shell.png" width=600>

The packet includes the vulnerable machine's IP address, so we can 

<img src="images/address.png" width=600>

We can use Python to send over the exact same payload, which will get the server to return the unredacted discord link.  

<img src="images/discord.png" width=600>

In the server, there is a `locations` channels that contains photos of the admins' current locations.  

<img src="images/locations.png" width=600>

A Google Lens search on the West location will lead us to Jurong Regional Library.  

<img src="images/library.png" width=600>

Flag: `YBN25{pE@NUT5_fOR_f1Nd!n6_U5}`