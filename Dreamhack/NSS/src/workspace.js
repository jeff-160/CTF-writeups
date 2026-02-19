const fs = require('fs');
const path = require("path");

const user_module = require('./user.js')
const check_session = user_module.check_session;
const users = user_module.users;

function cleanup_workspace(base_dir, workspace){
    for (const f_path in Object.values(workspace)) {
        fs.rmSync(path.join(base_dir, f_path), {recursive: true});
    }
}

module.exports = function (app) {
    app.get("/api/users/:userid", (req, res) => {
        const userid = req.params.userid || "";
        const token = req.body.token || "";

        if(!userid || !token)
            return res.status(400).json({ok: false, err: "Invalid userid or token"});
        if(!check_session(userid, token))
            return res.status(403).json({ok: false, err: "Failed to validate session"});

        const user = users[userid];
        res.status(200).json({ok: true, workspace: Object.keys(user.workspaces)});
    });

    app.post("/api/users/:userid", (req, res) => {
        const userid = req.params.userid || "";
        const token = req.body.token || "";
        const ws_name = req.body.ws_name || "";

        if(!userid || !token)
            return res.status(400).json({ok: false, err: "Invalid userid or token"});
        if(!check_session(userid, token))
            return res.status(403).json({ok: false, err: "Failed to validate session"});

        users[userid].workspaces[ws_name] = {};
        res.json({ok: true});
    });

    app.delete("/api/users/:userid", (req, res) => {
        const userid = req.params.userid || "";
        const token = req.body.token || "";
        const ws_name = req.body.ws_name || "";
        
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

        cleanup_workspace(workspace);
        delete user.workspace.ws_name;
        return res.status(200).json({ok: true});
    });
}

module.exports.cleanup_workspace = cleanup_workspace;
