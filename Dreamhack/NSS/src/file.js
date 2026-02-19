const fs = require('fs');
const path = require("path");

const user_module = require('./user.js')
const check_session = user_module.check_session;
const users = user_module.users;

function write_b64_file(f_path, contents) {
    try {
        if(!fs.existsSync(path.dirname(f_path)))
            fs.mkdirSync(path.dirname(f_path), {recursive: true});
        fs.writeFileSync(f_path, contents,{encoding: 'base64'});
    } catch (e) {
        fs.rmSync(f_path, {recursive: true});
        return false;
    }
    return true;
  }

function read_b64_file(f_path) {
    try{
        return fs.readFileSync(f_path, {encoding: 'base64'});
    } catch (e) {
        return;
    }
}

module.exports = function (app) {
    app.get("/api/users/:userid/:ws", (req, res) => {
        const userid = req.params.userid || "";
        const ws_name = req.params.ws || "";
        const token = req.body.token || "";

        if(!userid || !token)
            return res.status(400).json({ok: false, err: "Invalid userid or token"});

        if(!check_session(userid, token))
            return res.status(403).json({ok: false, err: "Failed to validate session"});

        const user = users[userid];
        if(!ws_name)
            return res.status(400).json({ok: false, err: "Invalid workspace name"});

        const workspace = user.workspaces[ws_name];
        if(!workspace)
            return res.status(404).json({ok: false, err: "Failed to find workspace"});
        
        res.status(200).json({ok: true, workspace: Object.keys(workspace)});
    });

    app.post("/api/users/:userid/:ws", (req, res) => {
        const userid = req.params.userid || "";
        const ws_name = req.params.ws || "";
        const token = req.body.token || "";
        const f_name = req.body.file_name || "";
        const f_path = req.body.file_path.replace(/\./g,'') || "";
        const f_content = req.body.file_content || "";

        if(!userid || !token)
            return res.status(400).json({ok: false, err: "Invalid id or token"});
        if(!check_session(userid, token))
            return res.status(403).json({ok: false, err: "Failed to validate session"});

        const user = users[userid];
        if(!ws_name)
            return res.status(400).json({ok: false, err: "Invalid workspace name"});

        const workspace = user.workspaces[ws_name];
        if(!workspace)
            return res.status(404).json({ok: false, err: "Failed to find workspace"});

        if(!f_name || !f_path)
            return res.status(400).json({ok: false, err: "Invalid file name or path"});

        if(!write_b64_file(path.join(user.base_dir, f_path), f_content))
            return res.status(500).json({ok: false, err: "Internal server error"});

        workspace[f_name] = f_path;
        return res.status(200).json({ok: true});
    });

    app.delete("/api/users/:userid/:ws", (req, res) => {
        const userid = req.params.userid || "";
        const ws_name = req.params.ws || "";
        const token = req.body.token || "";
        const f_name = req.body.file_name || "";
        
        if(!userid || !token)
            return res.status(400).json({ok: false, err: "Invalid userid or token"});
        if(!check_session(userid, token))
            return res.status(403).json({ok: false, err: "Failed to validate session"});

        const user = users[userid];
        if(!ws_name)
            return res.status(400).json({ok: false, err: "Invalid workspace name"});

        const workspace = user.workspaces[ws_name];
        if(!workspace)
            return res.status(404).json({ok: false, err: "Failed to find workspace"});

        if(!f_name)
            return res.status(400).json({ok: false, err: "Invalid file name"});

        const f_path = workspace[f_name];
        if(!f_path)
            return res.status(404).json({ok: false, err: "Failed to find file"});

        fs.rmSync(path.join(user.base_dir, f_path), {recursive: true});
        delete workspace[f_name];
        return res.status(200).json({ok: true});
    });

    app.get("/api/users/:userid/:ws/:fname", (req, res) => {
        const userid = req.params.userid || "";
        const ws_name = req.params.ws || "";
        const f_name = req.params.fname || "";
        const token = req.body.token || "";

        if(!userid || !token)
            return res.status(400).json({ok: false, err: "Invalid userid or token"});
        if(!check_session(userid, token))
            return res.status(403).json({ok: false, err: "Failed to validate session"});

        const user = users[userid];
        if(!ws_name)
            return res.status(400).json({ok: false, err: "Invalid workspace name"});
       
        const workspace = user.workspaces[ws_name];
        if(!workspace)
            return res.status(404).json({ok: false, err: "Failed to find workspace"});

        if(!f_name)
            return res.status(400).json({ok: false, err: "Invalid file name"});

        const f_path = workspace[f_name];
        if(!f_path)
            return res.status(404).json({ok: false, err: "Failed to find file"});
        
        const content = read_b64_file(path.join(user.base_dir, f_path));
        if(typeof content == "undefined")
            return res.status(500).json({ok: false, err: "Internal server error"});

        res.status(200).json({ok: true, file_content: content});
    });
}
