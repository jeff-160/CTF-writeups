## ligma nuts

Category: Rev  
Difficulty: Easy(?)

i forgot to screenshot the challenge details...  

We are provided with ane executable, and upon running, it appears to execute a series of randomly ordered checks to check if our system is a supposed supercomputer, but always inevitably fails before all checks pass.  

<img src="images/challenge.png" width=400>

Upon inspection, my teammate identified it as a .Net executable.  

<img src="images/type.jfif" width=400>

Decompiling the executable in Dnspy, I managed to locate the checks in the main program code, and overwrote them as anonymous functions that always returned `true`.  

<img src="images/checks.jpeg" width=600>

After all the checks passed, the program ran a series of finalisation checks. Going down the trail and overwriting the checks led me to the final part of the program that outputted the flag.  

<img src="images/printflag.jpeg" width=600>

After recompiling and running the modified executable, my teammate got the flag (the front portion was ommitted but since the flag format is known, this is insignificant).

`??: ??C25{w0w_c3rt1f13d_r3v_3ng1n33r}`