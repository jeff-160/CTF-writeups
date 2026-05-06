const express = require('express');
const cookieParser = require('cookie-parser');
const axios = require('axios');
const { spawn } = require('child_process');

const app = express();
const PORT = 3000;

const REGEX = /a|d|m|i|n|f|l|g/g;
const METHODS = ['GET', 'POST', 'DELETE', 'PUT']

app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());

app.get("/", (req, res) => {
    return res.send("Enjoy your test!");
})

app.post("/test", async (req, res) => {
    const { body, headers } = req;

    let METHOD = 'GET'
    let AUTH = ''
    let PATH = '/'
    let URL = "http://api.app.com:8000/api/v1"
    let HMAC = ''

    if (body.method){
        for (let i =0; i < METHODS.length; i++){
            if (METHODS[i] === body.method.toUpperCase()) {
                console.log(body.method.toUpperCase());
                METHOD = body.method.toUpperCase();
                break;
            }
        }

    } else{
        return res.status(400).send('Set Method.');
    }
    
    if (!req.cookies.auth) return res.status(401).send('Auth first.');

    else{
        if(Buffer.from(req.cookies.auth, 'base64').toString('utf8').startsWith('admin')) AUTH = 'admin'
        else AUTH = 'guest';
    }

    URL = URL + '/' + AUTH;

    if (REGEX.test(AUTH + req.body.path)) {
        return res.status(400).send('Invalid Character.');
    }

    
    if(req.body.path && req.body.path !== ""){

        if (body.path.startsWith("/")) {
            URL = URL + body.path; 
            PATH = '/api/v1/' + AUTH + body.path;
        } else{
            URL = URL + "/" + body.path; 
            PATH = '/api/v1/' + AUTH + '/' + body.path;
        }
    }
    
    const curlArgs = ["-X", body.method.toUpperCase(), URL];
    
    try {
        const data = {secret_key: Buffer.from(req.cookies.auth, 'base64').toString('utf8'), path: PATH}
        const response = await axios.post(`http://api.app.com:8000/api/v1/admin/getSignature`,data);
        HMAC = response.data.message
        curlArgs.push("-H", `X-Authorization: ${HMAC}`);

    } catch (e) {
        console.log(`Axios Error: ${e}`);
        return res.status(500).send('Error fetching data');
    }
    
    for (const [key, value] of Object.entries(headers)) {
        if (!["host","connection", "content-type", "content-length"].includes(key.toLowerCase())) {
            curlArgs.push("-H", `${key}: ${value}`);
        }
    }    

    if (METHOD === 'POST' || METHOD === 'PUT') {
        if (!req.body.title || !req.body.content){
            return res.status(400).send('At least one parameter is missing.')
        } else {
            const jsonData = JSON.stringify({
                title: req.body.title,
                content: req.body.content,
            });
            curlArgs.push("-H", "Content-Type: application/json");
            curlArgs.push("-d", jsonData);
        }
    }

    const curl = spawn("curl", curlArgs);

    let stdout = "";
    let stderr = "";

    curl.stdout.on("data", (data) => {
        stdout += data.toString();
    });

    curl.stderr.on("data", (data) => {
        stderr += data.toString();
    });

    curl.on("close", (code) => {
        if (code === 0) {
            return res.send(stdout);
        } else {
            return res.status(500).json({ error: stderr || "Unknown error occurred" });
        }
    });
});

app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
