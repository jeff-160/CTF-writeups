const crypto = require('crypto');
const Iconv = require('iconv').Iconv;
const { generateMD5Hash } = require('../utils');
const router = require('express').Router();
const { db, createMemo } = require('../db');
const { info } = require('console');

const DEFAULT_NONCE = process.env.NONCE || '30502580d81f844336d204b5f6ff1a84';
const denyList = ["<", ">", "!", "\\x", "\\u", "#"];
const encodingList = [
    "UTF-8","UTF-16","UTF-16LE","UTF-16BE","UTF-32","UTF-32LE","UTF-32BE",
    "ISO-8859-1","ISO-8859-2","ISO-8859-3","ISO-8859-4","ISO-8859-5","ISO-8859-6","ISO-8859-7","ISO-8859-8","ISO-8859-9","ISO-8859-10","ISO-8859-13","ISO-8859-14","ISO-8859-15","ISO-8859-16",
    "CP1250","CP1251","CP1252","CP1253","CP1254","CP1255","CP1256","CP1257","CP1258",
    "KOI8-R","KOI8-U",
    "EUC-JP", "EUC-KR",
    "SHIFT_JIS",
    "GB2312",
    "GBK",
    "GB18030",
    "BIG5","BIG5-HKSCS",
    "ARMSCII-8",
    "TCVN",
    "GEORGIAN-ACADEMY", "GEORGIAN-PS",
    "PT154",
    "RK1048",
    "MULELAO-1",
    "TIS-620",
    "CP874",
    "VISCII",
    "ISO-2022-JP","ISO-2022-KR","ISO-2022-CN"
];

router.get("/create", (req, res)=>{
    res.render('create', { encodingList });
})

router.post("/create", (req, res)=>{
    const { content, sourceEncoding } = req.body;
    const random = Math.random().toString();
    const memoId = generateMD5Hash(random);

    if (content === "" || sourceEncoding === ""){
        return res.status(403).send({result: false, msg: 'Missing param'});
    }

    let isDenied = false;

    denyList.forEach((chr) => {
        if (content.indexOf(chr) !== -1) {
            isDenied = true;
        }
    })
    
    if (isDenied) {
        return res.status(403).send({result: false, msg: 'Not allowed character'});
    }

    // console.log(`[+] id ==> ${memoId}`)
    try{
        const iconv = new Iconv(sourceEncoding, 'ASCII//TRANSLIT//IGNORE');
        const contentResult = iconv.convert(content);
        createMemo(memoId, contentResult, sourceEncoding);

    }catch (e){
        return res.status(500).send({result: false, msg: e, data: {content, sourceEncoding, random}});
    }

    return res.status(200).send({result: true, msg: 'Ok'});

})


router.get("/test", (req, res) => {
    const memo= 'you can test all the things';
    res.render('test', { encodingList: encodingList, memo: memo });
})

router.post("/test", (req, res) => {
    const { content, sourceEncoding } = req.body;

    if (content === "" || sourceEncoding === ""){
        return res.status(403).send({result: false, msg: 'Missing param'});
    }

    let isDenied = false;

    denyList.forEach((chr) => {
        if (content.indexOf(chr) !== -1) {
            isDenied = true;
        }
    })
    
    if (isDenied) {
        return res.status(403).send({result: false, msg: 'Not allowed character'});
    }
    try{
        const iconv = new Iconv(sourceEncoding, 'ASCII//TRANSLIT//IGNORE');
        const contentResult = iconv.convert(content);
        return res.render('test', {memo: contentResult.toString(), encodingList: encodingList});

    }catch (e){
        const contentResult = e
        return res.render('test', {memo: contentResult.toString(), encodingList: encodingList});
    }

    
})


router.get('/check', (req, res) => {
    if (req.ip.indexOf('127.0.0.1') == -1){
        
        return res.redirect('/home/smile');
    }
    const id = req.query.id;

    if (id === undefined){
        return res.render('check', {content: undefined, sourceEncoding: undefined, msg: 'Missing param'});
    }
    if (db.memo[id] === undefined){
        return res.render('check', {content: undefined, sourceEncoding: undefined, msg: 'Memo is not available'});
    }
    const content = db.memo[id].content;
    const sourceEncoding = db.memo[id].sourceEncoding;

    const nonce = (!req.session.nonce) ? DEFAULT_NONCE : req.session.nonce;
    res.setHeader('Content-Security-Policy', `default-src 'self'; base-uri 'self'; script-src 'nonce-${nonce}'`);
    return res.render('check', {content: content, sourceEncoding: sourceEncoding});
})

module.exports = router