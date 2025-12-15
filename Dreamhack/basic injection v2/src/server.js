const express = require('express');
const ejs = require('ejs');
const app = express();

app.use(express.urlencoded({ extended: true }));
app.use(express.json());

app.get('/', (req, res) => {
    const { username, settings } = req.query;
    
    if (!username) {
        return res.send('Missing param');
    }
    
    const ban = ['require', 'readFileSync', 'mainModule', 'throw', 'fs', '+', 'flag', 'exec', 'concat', 'split', 'Object', '\', \\', '=>', '*', 'x', '()', 'global', 'return', 'str', 'constructor', 'eval', 'replace', 'from', 'char', 'catch'];
    const u = username.toLowerCase();
    const s = settings ? settings.toLowerCase() : '';
    
    for (const b of ban) {
        if (u.includes(b) || s.includes(b)) {
            return res.send('nope! ヾ (✿＞﹏ ⊙〃)ノ');
        }
    }
    
    try {
        const template = '<h1>Welcome <%= username %>!</h1>';
        
        let opts = {};
        if (settings) {
            try {
                opts = JSON.parse(settings);
            } catch (e) {
                opts = {};
            }
        }
        
        let result;
        try {
            result = ejs.render(template, { username }, opts);
        } catch (renderError) {
            result = renderError.toString();
        }

        const limit = result.toString().slice(0, 35);
        
        res.send(limit);
    } catch (error) {
        const errorMsg = error.toString().slice(0, 35);
        res.status(500).send(errorMsg);
    }
});

const PORT = 5000;
app.listen(PORT, () => {
});