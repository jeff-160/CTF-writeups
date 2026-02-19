const crypto = require('crypto');
const fs = require('fs');
const os = require('os');
const path = require('path');
const appPrefix = 'nss';

users = {};
tokens = {};
salt = crypto.randomBytes(128).toString('base64');

function check_session(userid, token) {
    const sess = tokens[token]
    if(!sess) return false;
    if(sess.owner != userid) return false;
    if(sess.expire < Date.now() / 1000){
        tokens.delete(token);
        return false;
    }
    else return true;
}

function cleanup_user(user) {
    fs.rmSync(user.base_dir, {recursive: true});
};

module.exports = function (app) {
    app.get("/api/users", (req, res) => {
        res.status(200).json({res: true, users: Object.keys(users)});
    });

    app.post("/api/users", (req, res) => {
        const userid = req.body.userid || "";
        const pass = req.body.pass || "";
        if(!userid || !pass)
            return res.status(400).json({ok: false, err: "Invalid userid or password"});
        if(pass.length < 10)
            return res.status(400).json({ok: false, err: "Password too short"});
        const user = users[userid];
        if(user)
            return res.status(400).json({ok: false, err: "ID already exists"});

        base_dir = ""
        try {
            base_dir = fs.mkdtempSync(path.join(os.tmpdir(), appPrefix));
            }
        catch {
            return res.status(500).json({ok: false, err: "Internal server error"});
        };
        if(!base_dir) 
            return res.status(500).json({ok: false, err: "Internal server error"});
            
        
        users[userid] = {
            userid : userid,
            pass : crypto.createHash('sha512').update(pass + salt).digest('hex'),
            workspaces : {},
            base_dir: base_dir
        };
        res.json({ok: true});
    });
    
    app.delete("/api/users", (req, res) => {
        const userid = req.body.userid || "";
        const pass = req.body.pass || "";
        if(!userid || !token)
            return res.status(400).json({ok: false, err: "Invalid userid or token"});
        if(!check_session(userid, token))
            return res.status(403).json({ok: false, err: "Failed to validate session"});
        
        const user = users[userid];

        cleanup_user(user);
        delete users.userid;
        return res.status(200).json({ok: true});
    });

    
    app.post("/api/users/auth", (req, res) => {
        const userid = req.body.userid || "";
        const pass = req.body.pass || "";
        if(!userid || !pass)
            return res.status(400).json({ok: false, err: "Invalid userid or password"});

        const user = users[userid];
        if(!user)
            return res.status(404).json({ok: false, err: "Failed to find user"});

        if(user.pass != crypto.createHash('sha512').update(pass + salt).digest('hex'))
            return res.status(403).json({ok: false, err: "Incorrect password"});
        
        token = crypto.randomBytes(20).toString('hex');
        tokens[token] = {
            owner : userid,
            expire: 30 * 60 + Date.now() / 1000
        };
        res.json({ok: true, token: token});
    });
}

module.exports.check_session = check_session;
module.exports.users = users;
module.exports.tokens = tokens;
