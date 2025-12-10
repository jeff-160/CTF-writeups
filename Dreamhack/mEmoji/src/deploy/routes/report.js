const router = require('express').Router();
const { bot } =require('../utils');

router.get('/', (req, res)=>{
    let msg = undefined;
    return res.render('report', {msg: msg});
})

router.post('/', async (req, res) => {
    const { path, memoId } = req.body;

    if (bot(path, memoId)) {
        return res.render('report', {msg: 'Ok'});
    }else{
        return res.render('report', {msg: 'Fail'});
    }
})
module.exports = router