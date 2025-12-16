const express = require('express');
var path = require('path');
const app = express();
const port = 3000;
 
app.set('views', path.join(__dirname, '/templates'));
app.set('view engine', 'ejs');
app.use(express.urlencoded({ extended: true }));

app.get('/', (req, res) => {
   res.render('index', req.query )
})
 
app.listen(port, () => {})
