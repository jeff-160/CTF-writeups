const express = require("express");
const routerFlag = require("./routes/flag");
const cookieParser = require("cookie-parser");
const routerAdmin = require("./routes/admin");
const { auth } = require("./middleware/auth");

const app = express();
const PORT = 3000;

app.use(cookieParser());
app.use(express.static('public'));
app.use(express.urlencoded({
    extended: false
}));

app.use("/admin",routerAdmin);
app.use("/flag",routerFlag);

app.get("/", auth, (req, res) => {
    res.redirect("/admin");
})

app.listen(PORT,()=>{
    console.log(`[+] Start on port ${PORT}`);
})