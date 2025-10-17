const fs = require('fs');
const express = require('express');

const port = 8000;
const flag = fs.readFileSync('flag.txt', 'utf8');

const app = express();
app.use(express.urlencoded({ extended: false }));

app.get('/', (req, res) => {
    res.send(`I am so lazy to make a frontend :)`);
});

app.get('/flag', (req, res) => {
    res.send(`WaRP{REDACTED}`);
});

app.post('/', (req, res) => {
    const input_str = req.body.input_str.toString() || '';
    if (!input_str.includes('[') && !input_str.includes(']')) {
        if (!input_str.includes('+') || input_str.split('+').slice(1).every(part => part.startsWith('='))) {
            if (input_str.length <= 6 && (eval(input_str) > 0) == false && (eval(input_str) == 0) == false && (eval(input_str) >= 0) == true) {
                res.redirect('/flag')
            }
        }
    }
    res.redirect('/');
});

app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});