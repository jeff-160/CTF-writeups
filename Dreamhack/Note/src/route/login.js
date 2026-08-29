const express = require("express")
const router = express.Router()

const { checkLogin, getBodyToList, format } = require("../util.js")

router.get("/login", (req, res) => {
    if(req.session.isLogin){
        return res.redirect("/")
    }

    return res.render("login", {
        "data" : {}
    })
})

router.post("/login", async (req, res) => {
    if (req.session.isLogin == true) {
        return res.redirect("/")
    }

    const args = getBodyToList(req.body)
    if (args == -1){
        return res.send("You can only input to 200 lengths.")
    }
    const db = req.app.get("db")

    try {
        const row = await db.select("SELECT * FROM USER where id=\"%s\" and pw=\"%s\"", args)
        
        if (row) {
            req.session.isLogin = true
            req.session.userid = row["id"]
            return res.redirect("/")
        } 
        else {
            return res.render("login", {
                "data" : {
                    "result": "error",
                    "message": format("Login fail. [id: %s] [pw: %s]", args)
                }
            })
        }
    } 
    catch (error) {
        return res.status(500).send(error)
    }
})

router.get("/logout", (req, res) => {
    req.session.isLogin = false
    req.session.userid = undefined

    return res.redirect("/user/login")
})

module.exports = router