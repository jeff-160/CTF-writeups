<img src="images/challenge.png" width=600>

We are provided with a file that contains GCode commands.  

<img src="images/gcode.png" width=500>

Running it in an [online viewer](https://ncviewer.com/) reveals a model of a fox, along with a suspicious looking cuboid.  

<img src="images/model.jpeg" width=600>

Looking back at the challenge file, there is only 1 section inside that uses highly precise floating point coordinates.  

<img src="images/floats.png" width=400>

These are actually IEEE-754 float32 bytes, and we can concatenate and decode them as UTF-16-LE.  

This reveals another cipher, along with source code of a rotation encryption function.  

<img src="images/decoded.png" width=600>

We can simply reverse the encryption and write a script to bruteforce the encryption key.  

<img src="images/flag.png" width=600>