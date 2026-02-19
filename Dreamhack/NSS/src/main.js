const express = require("express");
const bodyParser = require('body-parser');
const app = express(); 

app.use(bodyParser.json());

app.listen(80, () => console.log("[*] Server Started!"));

app.get("/", (req, res) => {
    res.status(204);
});

require('./user.js')(app);
require('./workspace.js')(app);
require('./file.js')(app);



