const express = require("express")
const session = require("express-session")
const crypto = require('crypto')

const router_login = require("./route/login")
const router_index = require("./route/index")
const sqlite = require("./db/db")

const app = express()
const PORT = process.env.port || 3000
const db = new sqlite(":memory:")

app.set("db", db)
app.set("view engine", "ejs")
app.use(express.static(__dirname + "/static"))
app.use(express.urlencoded({
    extended: false
}))
app.use(session({
    secret: crypto.randomBytes(32).toString()
}));

app.use("/", router_index)
app.use("/user", router_login)

app.listen(PORT, () => {
    console.log("Enjoy")
})