## Welcome Welcome

<img src="images/chall.png" width=400>

We are provided with a webpage where we can enter a name to display a welcome message.  

<img src="images/webpage.png" width=400>

The webpage uses a `contexts` dictionary to render different templates depending on the user.  The admin context is stored with a randomly generated name, and will display the flag when rendered.  

<img src="images/contexts.png" width=600>

Looking at the source code, we notice that there is an SSTI vulnerability, as the `render()` method of the `Context` class passes in the current context instance to be formatted.  

<img src="images/vuln.png" width=400>

We can easily leak all global variables from the `Context` instance through an attribute chain, allowing us to view the admin's name.  

```
{self.__class__.__init__.__globals__}
```

<img src="images/globals.png" width=600>

After entering the admin's name, we are able to get the flag.  

<img src="images/flag.png" width=600>