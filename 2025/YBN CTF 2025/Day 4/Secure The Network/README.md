## Secure The Network  

<img src="images/chall.png" width=600>

This challenge requires us to answer `9` questions correctly to get the flag, and provides us with a packet capture and system logs for us to analyse.  

### Question 1  

<img src="images/qn1.png" width=600>

Filtering for `http` packets in the capture shows numerous requests being made from `120.225.134.131` to the target machine, and it looks like their enumerating the directories, so this is our attacker address.  

<img src="images/enumerate.png" width=600>

### Question 2  

<img src="images/qn2.png" width=600>

We can locate the packet where the attacker makes a request to the root directory of the web server (`GET /`). Following the TCP stream will show the full HTML source of the web server, which contains a reference to `Wordpress`.   

<img src="images/wordpress.png" width=600>

### Question 3  

<img src="images/qn3.png" width=600>

To answer this question, we can filter with `http.request.method=="GET"` to get all packets of the attacker bruteforcing subdirectories.  

<img src="images/bruteforce.png" width=600>

We can select one of the packets and the `User-Agent` header will show `gobuster` is being used to perform the enumeration.  

<img src="images/gobuster.png" width=600>

### Question 4  

<img src="images/qn4.png" width=600>

In the packet capture, we can see that the attacker bruteforces `GET` requests for wordpress plugins. We can filter with `http.request.uri contains "wp-content/plugins" && http.response.code == 200 && http.request.uri contains "readme"` to get only the ones that were successfully fetched.  

<img src="images/plugins.png" width=600>

Following the TCP stream of one of the packets will show the documentation for the `file-manager` plugin, with the version number being `6.0`. In the answer format, we get: `file_manager:v6.0`.  

<img src="images/file_manager.png" width=600>

### Question 5  

<img src="images/qn5.png" width=600>

Since we already identified the vulnerable plugin and the version number, a quick google search will lead us to [CVE-2020-25213](https://nvd.nist.gov/vuln/detail/CVE-2020-25213), which details an RCE vulnerability that allows execution of arbitrary PHP, which is very evident in the packet capture.  

### Question 6  

<img src="images/qn6.png" width=600>

i lowk guessed this one ngl  

answer: `python3 -c "import pty;pty.spawn('/bin/bash')"`  

### Question 7  

<img src="images/qn7.png" width=600>

Since the file extension only has two characters, we can make an educated guess that they are most likely `.sh` files. A quick filter with `http.request.method=="GET" and frame contains "sh"` will show the files below.  

<img src="images/files.png" width=600>

### Question 8  

<img src="images/qn8.png" width=600>

From the packets above, if we remove the `.sh` filter, we can notice a `id_ed25519.pub` file being uploaded at around the same time. Since the filename matches the answer format exactly, this is our persistence file.  

<img src="images/pub.png" width=600>

### Question 9  

<img src="images/qn9.png" width=600>

Since `icmp` is used for host discovery, we can filter with `icmp.type == 0`, which will show the IP address `172.16.100.125`.  

<img src="images/icmp.png" width=600>

Submitting all the correct answers will then get the server to output the flag.  

Flag: `YBN{019aecc9843873b689b96225c1299939}`