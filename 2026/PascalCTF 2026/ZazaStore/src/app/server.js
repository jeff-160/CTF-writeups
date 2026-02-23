const express = require('express');
const path = require('path');
const session = require('express-session');
const app = express();
const PORT = 3000;

app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));

const content = {
    "RealZa": process.env.FLAG,
    "FakeZa": "pascalCTF{this_is_a_fake_flag_like_the_fake_za}",
    "ElectricZa": "<img src='images/ElectricZa.jpeg' alt='Electric Za'>",
    "CartoonZa": "<img src='images/CartoonZa.png' alt='Cartoon Za'>"
};
const prices = { "FakeZa": 1, "ElectricZa": 65, "CartoonZa": 35, "RealZa": 1000 };

app.use(session({
    secret: crypto.randomUUID(),
    resave: false,
    saveUninitialized: false,
    cookie: { secure: false }
}));

app.get('/', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/login');
    }
    return res.render('index', { balance: req.session.balance, prices: prices });
});

app.get('/login', (req, res) => {
    if (req.session.user) {
        return res.redirect('/');
    }

    res.render('login');
});

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

app.get('/cart', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/login');
    }
    res.render('cart', {
        cartObj: JSON.stringify(req.session.cart),
        pricesObj: JSON.stringify(prices)
    });
});

app.get('/inventory', (req, res) => {
    if (!req.session.user) {
        return res.redirect('/login');
    }

    res.render('inventory', { inventory: req.session.inventory, content: content });
});

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

app.get('/logout', (req, res) => {
    req.session.destroy(() => {
        res.redirect('/login');
    });
});

app.listen(PORT, () => console.log(`Server running on http://localhost:${PORT}`))