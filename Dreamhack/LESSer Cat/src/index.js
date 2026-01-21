const express = require('express');
const less = require("less");
const bodyParser = require('body-parser');
const crypto = require("crypto");
const fs = require("fs");
const path = require("path");

const app = express();
const port = 3000;

app.use(express.static( path.join(__dirname, '/static')));
app.use(bodyParser.urlencoded({ extended: true }));

admin_data = {
  "admin" : "c60f85df4cd2f4e0a50908ae9df30b952dc563ce32d6907740ee751b0138346b"
}

FLAG = fs.readFileSync('flag', "utf8");
fs.unlinkSync("flag");

function colorPicker(colorDict){

  var css = "";

  for (var key in colorDict){

    try{

      if(!colorDict[key].match(/^#[\w\d]{6}$/)) return false;

    } 
    catch(error){
      // console.log(error)
    }

    css += `@${key}:` + colorDict[key] + ";";

  }

  css = css + "body{ background-color: @bgcolor; color: @color; }";

  return css;
}

app.get('/', (req, res) => {

  path.join(__dirname + '/static/index.html');

})

app.get('/color', (req,res) => {
  res.sendFile(path.join(__dirname + '/static/color.html'));
})

app.post('/color', (req, res) => {

  const background = req.body.bgColor;

  const font = req.body.fontColor;

  if(background === undefined || font === undefined) return res.send("Set Your Color Code!");

  var colorDict = {
    "bgcolor" : background,
    "color" : font
  }

  var css = colorPicker(colorDict);

  if (css == false) return res.sendStatus(500);

  less.render(css.toString(), (error, output) => {
  
    if(error){
      return res.send(`Less Compile Error`);
    }

    fs.writeFileSync('./static/image.css', output['css']);
    
    return res.send(`ColorPicker Done`);
  
  })

})

app.get('/image', (req,res) => {
  res.sendFile(path.join(__dirname + '/static/image.html'));
})

app.post('/reset_mail', (req, res) => {

  // TODO
  // Make SMTP server later...

  fs.writeFileSync('./mail.log', crypto.randomBytes(16).toString('hex'));

  return res.send("Reset Mail Send.");

})

app.post('/pass_reset', (req, res) => {
  var reset_password = req.body.password;
  var reset_key = req.body.key;
  
  if(fs.existsSync("./mail.log")){

  
    if(fs.readFileSync('./mail.log', "utf8") == reset_key){

      admin_data = {
        "admin" : crypto.createHash('sha256').update(reset_password).digest('hex')
      };

      return res.send("Reset Done");
    }

  }else {

    return res.send("Reset Key is missing");

  }
  
  return res.send("Reset Key is invalid");
})

app.post('/login', (req,res) => {

  var username = req.body.username;
  var password = req.body.password;
  
  if(username == "admin"){
    if(crypto.createHash('sha256').update(password).digest('hex') == admin_data['admin']){
      return res.send(FLAG);
    }

    return res.send("Login fail");
  }

  return res.send("Admin Only");
})

app.listen(port, () => {
  console.log(`Server on http://localhost:${port}`);
});
