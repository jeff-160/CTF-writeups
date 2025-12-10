const fs = require('fs');
const path = require('path');
const router = require('express').Router();
const { generateMD5Hash } = require('../utils');


router.get('/nonce.png', (req, res) =>{
    const random = Math.random().toString();
    const nonce = generateMD5Hash(random);
    req.session.nonce = nonce;
    res.setHeader('Content-Type','image/png');
    return res.send('ok');
})

router.get("/:emoji", (req, res)=>{
    const emoji = req.params.emoji || 'smile';
    if (fs.existsSync(path.join(__dirname, `../static/img/${emoji}.png`))){
        return res.render('index', {emoji: `/static/img/${emoji}.png`});
    }else{
        return res.status(404).render('index', {emoji: undefined});
    }
    
})

    
module.exports = router