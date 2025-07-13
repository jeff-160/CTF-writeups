## ChooseOrDie

Category: Rev  
Difficulty: Medium

<img src="images/challenge.jpeg" width=400>

We are provided with a game executable that upon running, gives us a series of "Yes" or "No" prompts.  

<img src="images/game.png" width=600>

My teammate discovered that it was a C++ executable compiled with the .Net framework.  

<img src="images/type.jpeg" width=600>

After decompiling the executable in Jetbrains dotPeek, I was able to find the main game logic.  

The game prompts us with 16 questions, and combines all responses into a byte array (6 for "Yes" and 7 for "No"). The byte array is then hashed with MD5, and if it matches a hardcoded base64 hash, the game then gives us our flag.  

<img src="images/source.png" width=600>

Since there are only 65,536 possible combinations, we can easily bruteforce the combination of inputs that produces the desired hash.  

<img src="images/inputs.png" width=600>

After submitting the correct inputs, the game gives us the flag.  

<img src="images/flag.png" width=600>