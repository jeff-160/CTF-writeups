<?php

define('MESSAGE_FILE', '/messages.txt');
define('DATABASE_FILE', '/database/users.json');
define('WELCOME_FILE', './flag.txt');
define('SEEK', 6);


// Start sessions securely
ini_set('session.use_only_cookies', 1);
ini_set('session.use_strict_mode', 1);

session_set_cookie_params([
    'lifetime' => 86400,
    'path' => '/',
    'domain' => '',
    'secure' => isset($_SERVER['HTTPS']),
    'httponly' => true,
    'samesite' => 'Lax'
]);

session_start();

$db_file = __DIR__ . DATABASE_FILE;
if (!file_exists($db_file)) {
    file_put_contents($db_file, json_encode([]));
}

$file_path = __DIR__ . MESSAGE_FILE;

if (!file_exists($file_path)) {
    echo json_encode(['message' => 'setup err!']);
    exit;
}
else{
    $file = new SplFileObject($file_path, 'r');
    $file->seek(SEEK); 
    $sig = explode(':',$file->current())[1];
    $sigil = trim($sig);
}

if (empty($_SESSION['csrf_token'])) {
    $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
}
$URI = null;


function get_users() {
    global $db_file;
    $data = file_get_contents($db_file);
    return json_decode($data, true) ?: [];
}

function save_users($users) {
    global $db_file;
    file_put_contents($db_file, json_encode($users, JSON_PRETTY_PRINT));
}

function verify_csrf_token($token) {
    return isset($_SESSION['csrf_token']) && hash_equals($_SESSION['csrf_token'], $token);
}

function sanitizeUsername(string $username) {
    return basename(preg_replace('/[^a-zA-Z0-9_-]/', '', $username));
}

function sanitizeFilename(string $filename){
    $safe = str_replace(["/", "\\"], '', basename($filename));
    if (!str_ends_with($safe, '.png')) {
        $safe .= '.png';
    }
    return $safe;
}

function require_login() {
    if (empty($_SESSION['user_id'])) {
        header("Location: login.php");
        exit;
    }
}
