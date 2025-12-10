const express = require('express');
const session = require('express-session');
const crypto = require('crypto');
const path = require('path');
const routeMemo = require('./routes/memo');
const routeIndex = require('./routes/index');
const routeReport = require('./routes/report');

const app = express();
const PORT = process.env.PORT | 3000

app.set('views', path.join(__dirname, '/views'));
app.use('/static', express.static(path.join(__dirname, 'static')));
app.set("view engine", "ejs");
app.engine('ejs', require('ejs').__express);
app.use(express.urlencoded({extended: false}));
app.use(express.json());
app.use(session({
    secret: crypto.randomBytes(32).toString(),
    resave: false,
    saveUninitialized: true,  
}));
app.use('/memo', routeMemo);
app.use('/home', routeIndex);
app.use('/report', routeReport);

app.get('/', (req, res) => {
    res.redirect('/home/smile');
})

app.listen(PORT, ()=>{
    console.log(`[+] Start on port ${PORT}`);
})