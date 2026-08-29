const sqlite3 = require("sqlite3")
const { format } = require("../util.js")

class Database {
    constructor(filename) {
        this.db = new sqlite3.Database(filename)
        this.db.serialize(() => {
            this.db.run("CREATE TABLE user (id text, pw text)")
            this.db.run("CREATE TABLE board (idx INTEGER PRIMARY KEY AUTOINCREMENT, title text, content text, important INTEGER default 0)")
            this.execute("INSERT INTO user (id, pw) values (\"%s\", \"%s\")", ["guest", "guest"])
            this.execute("INSERT INTO board (title, content) values (\"%s\", \"%s\")", ["🚀 Hello", "You can use markdown."])
        })
    }

    select(query, args) {
        return new Promise((resolve, reject) => {
            this.db.get(format(query, args), (err, res) => {
                if (err) {
                    reject(err)
                } 
                else {
                    resolve(res)
                }
            })
        })
    }

    selectAll(query, args) {
        return new Promise((resolve, reject) => {
            this.db.all(format(query, args), (err, res) => {
                if (err) {
                    reject(err)
                } 
                else {
                    resolve(res)
                }
            })
        })
    }

    execute(query, args) {
        return new Promise((resolve, reject) => {
            this.db.run(format(query, args), (err, res) => {
                if (err) {
                    reject(err)
                } 
                else {
                    resolve(res)
                }
            })
        })
    }

}

module.exports = Database