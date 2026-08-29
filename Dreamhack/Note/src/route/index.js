const express = require("express")
const MarkdownIt = require("markdown-it")

const router = express.Router()
const md = new MarkdownIt()

const {checkLogin, getBodyToList} = require("../util")


router.get("/", checkLogin, async (req, res) => {
    if (req.session.userid != "admin"){
        return res.send("admin only")
    }

    try{
        const db = req.app.get("db")
        const row = await db.selectAll("SELECT * FROM board ORDER BY idx DESC", [])
        
        return res.render("index", {
            "data" : row
        })
    }
    catch {
        return res.send("something wrong").status(500)
    }
})

router.post("/write", checkLogin, async (req, res) => {
    if (req.session.userid != "admin"){
        return res.json({
            "result" : "error",
            "message" : "only admin"
        })
    }

    const args = getBodyToList(req.body)
    if (args == -1){
        return res.json({
            "result" : "error",
            "message" : "You can only input to 200 lengths."
        })
    }
    const db = req.app.get("db")
    
    try {
        await db.execute("INSERT INTO board (title, content) values (\"%s\", \"%s\")", [args[0], md.render(args[1])])
        return res.redirect("/")
    }
    catch {
        return res.send("something wrong").status(500)
    }
})

router.get("/preview", checkLogin, async (req, res) => {
    if (req.session.userid != "admin"){
        return res.json({
            "result" : "error",
            "message" : "only admin"
        })
    }

    try{
        req.query.content = md.render(req.query.content)

        return res.render("preview", req.query)
    }
    catch{
        return res.send("Something wrong").status(500)
    }
})

router.get("/important", checkLogin, async (req, res) => {
    if (req.session.userid != "admin"){
        return res.json({
            "result" : "error",
            "message" : "only admin"
        })
    }

    const idx = req.query.idx
    const db = req.app.get("db")

    try{
        const row = await db.select("SELECT important FROM board WHERE idx = %d", [idx])
        
        if(row){
            await db.execute("UPDATE board SET important = %d WHERE idx = %d", [1 - row.important, idx])
            return res.json({
                "result" : "success"
            })
        }
        else{
            throw new Error("Post not exist")
        }
    }
    catch{
        return res.json({
            "result" : "error",
            "message" : "something wrong"
        })
    }
})

module.exports = router